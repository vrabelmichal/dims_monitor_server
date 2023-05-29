import json
import logging

from django.db import transaction, IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ListSerializer

from rest_server.models import Report, Station
from rest_server.serializers.camera_status import CameraStatusNestedSerializer
from rest_server.serializers.env_log_measurement import EnvironmentLogUploadSerializer
from rest_server.serializers.process import ProcessSerializer
from rest_server.serializers.ufo_capture_output import UfoCaptureOutputNestedSerializer, \
    short_description_of_data as ufo_short_description_of_data
from rest_server.serializers.cpu_status import CpuStatusNestedSerializer
from rest_server.serializers.disk_usage import DiskUsageNestedSerializer
from rest_server.serializers.memory_usage import MemoryUsageNestedSerializer
from rest_server.serializers.ohm_measurement import OhmSensorMeasurementNestedSerializer

from django.conf import settings

# MODULE_SERIALIZER_MAPPING = dict(
#     disk_usage=DiskUsageNestedSerializer,
#     cpu_status=CpuStatusNestedSerializer
# )

ACQUIRED_MODULES = [
    'disk_usage', 'memory_usage', 'processes', 'cpu_status', 'camera_status',
    'ohm',
    'ufo_capture_output',
    'environment_log'
]

INTEGRITY_ERROR_DATA_DESCRIPTION_FUNCS = dict(
    ufo_capture_output=ufo_short_description_of_data
)


class ReportNestedSerializer(serializers.ModelSerializer):

    # station is created in views.rest.report.post
    station = serializers.SlugRelatedField(
        many=False, read_only=False, required=True,
        slug_field='name', queryset=Station.objects.all()
    )

    disk_usage = DiskUsageNestedSerializer(many=True, read_only=False, required=False)
    memory_usage = MemoryUsageNestedSerializer(many=True, read_only=False, required=False)
    cpu_status = CpuStatusNestedSerializer(many=True, read_only=False, required=False)
    camera_status = CameraStatusNestedSerializer(many=True, read_only=False, required=False)
    ohm = OhmSensorMeasurementNestedSerializer(many=True, read_only=False, required=False)
    ufo_capture_output = UfoCaptureOutputNestedSerializer(many=True, read_only=False, required=False)
    environment_log = EnvironmentLogUploadSerializer(many=True, read_only=False, required=False)
    processes = ProcessSerializer(many=True, read_only=False, required=False)

    attachments = serializers.DictField(    # module
        child=serializers.DictField(        # entry
            child=serializers.DictField(    # file
                child=serializers.FileField(allow_empty_file=True)
            )
        ),
        read_only=False,
        required=False
    )

    is_backfill = serializers.BooleanField(required=False, default=False)

    _logger = None

    class Meta:
        model = Report
        fields = ['start_utc', 'post_utc', 'retrieved_utc', 'hash', 'station', 'attachments', 'is_backfill',
                  *ACQUIRED_MODULES]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._logger = logging.getLogger('dims_monitor_server.rest_server.serializers.ReportNestedSerializer')

    def create(self, validated_data):

        module_data_dict = dict()

        for module_name in ACQUIRED_MODULES:
            if module_name in validated_data:
                module_data_dict[module_name] = validated_data.pop(module_name)

        if 'attachments' in validated_data:
            attachments = validated_data.pop('attachments')
        else:
            attachments = dict()

        integrity_errors_dict = dict()

        is_backfill = validated_data.pop('is_backfill', False)

        with transaction.atomic():
            transaction.on_commit(lambda: self._logger.debug('ReportNestedSerializer: outer transaction commit'))

            report = Report.objects.create(**validated_data)

            for module_name, module_data in module_data_dict.items():
                if not isinstance(module_data, (list, tuple)):
                    module_data = [module_data]

                module_serializer = self.fields.fields.get(module_name)
                if module_serializer is None:
                    # This should never happen
                    raise RuntimeError(f'Invalid module name: "{module_name}"')

                if isinstance(module_serializer, ListSerializer):
                    module_serializer = module_serializer.child

                module_serializer_cls = module_serializer.__class__

                for measurement_i, module_data_entry in enumerate(module_data):
                    # This might not be an ideal approach because the validation might be reselecting data
                    #   from the database
                    # Probably a different kind of serializer might be better or it should be implemented
                    #   in another more efficient way

                    module_data_entry['report'] = report.id
                    module_data_entry['station'] = report.station.id

                    if module_name in attachments:
                        str_measurement_i = str(measurement_i)
                        if str_measurement_i in attachments[module_name]:
                            for file_k, file_field_v in attachments[module_name][str_measurement_i].items():
                                module_data_entry[file_k] = file_field_v

                    ds = module_serializer_cls(data=module_data_entry)

                    if ds.is_valid(raise_exception=True):
                        # for now, integrity errors are ignored
                        try:
                            with transaction.atomic():
                                transaction.on_commit(
                                    lambda: self._logger.debug('ReportNestedSerializer: inner transaction commit'))
                                ds.save()
                        except IntegrityError as e:
                            if module_name not in integrity_errors_dict:
                                integrity_errors_dict[module_name] = []
                            # entry_hash = hash(frozenset(sorted(module_data_entry.items())))
                            # integrity_errors_dict[module_name].append(entry_hash)
                            integrity_errors_dict[module_name].append(module_data_entry)

                            # try:
                            #     module_data_entry_str = json.dumps(module_data_entry)
                            # except Exception as e:
                            #     module_data_entry_str = '[Failed to encode:]' + str(module_data_entry)

                            if settings.DEBUG or not is_backfill:
                                module_data_entry_str = '[Integrity error]'
                                if module_name in INTEGRITY_ERROR_DATA_DESCRIPTION_FUNCS:
                                    module_data_entry_str += \
                                        INTEGRITY_ERROR_DATA_DESCRIPTION_FUNCS[module_name](module_data_entry)
                                else:
                                    module_data_entry_str += str(module_data_entry)

                                maybe_dots_str = '...' if len(module_data_entry_str) > 255 else ''
                                self._logger.log(
                                    logging.DEBUG if self.is_backfill else logging.WARNING,
                                    f'Integrity error in report #{report.id} is being ignored '
                                    f'(module: {module_name}, entry: {module_data_entry_str[:255]}{maybe_dots_str})'
                                )

            if len(integrity_errors_dict) == 0:
                report.fully_processed = True  # now used to indicate processing errors
            else:
                report.integrity_errors = integrity_errors_dict

            report.save()  # either fully processed or integrity errors

        return report
