import logging

from django.db import transaction, IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ListSerializer

from rest_server.models import Report, Station
from rest_server.serializers.ufo_capture_output import UfoCaptureOutputNestedSerializer
from rest_server.serializers.cpu_status import CpuStatusNestedSerializer
from rest_server.serializers.disk_usage import DiskUsageNestedSerializer
from rest_server.serializers.memory_usage import MemoryUsageNestedSerializer
from rest_server.serializers.ohm_measurement import OhmSensorMeasurementNestedSerializer

# MODULE_SERIALIZER_MAPPING = dict(
#     disk_usage=DiskUsageNestedSerializer,
#     cpu_status=CpuStatusNestedSerializer
# )

ACQUIRED_MODULES = ['disk_usage', 'memory_usage',
                    'cpu_status', 'ohm', 'ufo_capture_output']


class ReportNestedSerializer(serializers.ModelSerializer):

    station = serializers.SlugRelatedField(
        many=False, read_only=False, required=True,
        slug_field='name', queryset=Station.objects.all()
    )

    disk_usage = DiskUsageNestedSerializer(many=True, read_only=False, required=False)  # intentionally singular
    memory_usage = MemoryUsageNestedSerializer(many=True, read_only=False, required=False)  # intentionally singular
    cpu_status = CpuStatusNestedSerializer(many=True, read_only=False, required=False)
    ohm = OhmSensorMeasurementNestedSerializer(many=True, read_only=False, required=False)
    ufo_capture_output = UfoCaptureOutputNestedSerializer(many=True, read_only=False, required=False)

    attachments = serializers.DictField(    # module
        child=serializers.DictField(        # entry
            child=serializers.DictField(    # file
                child=serializers.FileField()
            )
        ),
        read_only=False,
        required=False
    )

    _logger = None

    class Meta:
        model = Report
        fields = ['start_utc', 'post_utc', 'retrieved_utc', 'hash', 'station', 'attachments', *ACQUIRED_MODULES]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._logger = logging.getLogger('rest_server.ReportNestedSerializer')

    def create(self, validated_data):

        module_data_dict = dict()

        for module_name in ACQUIRED_MODULES:
            if module_name in validated_data:
                module_data_dict[module_name] = validated_data.pop(module_name)

        if 'attachments' in validated_data:
            attachments = validated_data.pop('attachments')
        else:
            attachments = dict()

        # TODO create with non-existing station should be tested !
        # XXXXXXXXXXXXXXXXXXX get_or_create should be tested when no id is provided
        # XXXXXXXXXXXXXXXXXXX report, report_was_created = Report.objects.get_or_create(**validated_data)

        integrity_errors_dict = dict()

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
                            entry_hash = hash(frozenset(sorted(module_data_entry.items())))
                            integrity_errors_dict[module_name].append(entry_hash)
                            self._logger.warning(
                                f'Integrity error in report #{report.id} is being ignored '
                                f'(module: {module_name}, entry hash: {integrity_errors_dict[module_name]})'
                            )

            if len(integrity_errors_dict) == 0:
                report.fully_processed = True  # now used to indicate processing errors
            else:
                report.integrity_errors = integrity_errors_dict

            report.save()  # either fully processed or integrity errors

        return report
