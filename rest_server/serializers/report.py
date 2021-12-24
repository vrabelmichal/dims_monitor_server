from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ListSerializer

from rest_server.models import Report
from rest_server.serializers.cpu_status import CpuStatusNestedSerializer
from rest_server.serializers.disk_usage import DiskUsageNestedSerializer
from rest_server.serializers.memory_usage import MemoryUsageNestedSerializer
from rest_server.serializers.ohm_measurement import OhmSensorMeasurementNestedSerializer

# MODULE_SERIALIZER_MAPPING = dict(
#     disk_usage=DiskUsageNestedSerializer,
#     cpu_status=CpuStatusNestedSerializer
# )

ACQUIRED_MODULES = ['disk_usage', 'memory_usage',
                    'cpu_status', 'ohm']


class ReportNestedSerializer(serializers.ModelSerializer):

    disk_usage = DiskUsageNestedSerializer(many=True, read_only=False, required=False)  # intentionally singular
    memory_usage = MemoryUsageNestedSerializer(many=True, read_only=False, required=False)  # intentionally singular
    cpu_status = CpuStatusNestedSerializer(many=True, read_only=False, required=False)
    ohm = OhmSensorMeasurementNestedSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = Report
        fields = ['start_utc', 'retrieved_utc', 'hash', 'station', *ACQUIRED_MODULES]

    def create(self, validated_data):

        module_data_dict = dict()

        for module_name in ACQUIRED_MODULES:
            if module_name in validated_data:
                module_data_dict[module_name] = validated_data.pop(module_name)

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

            for module_data_entry in module_data:
                module_data_entry['report'] = report.id
                # ds = MODULE_SERIALIZER_MAPPING[module_name](data=module_data_entry)
                ds = module_serializer_cls(data=module_data_entry)
                if ds.is_valid(raise_exception=True):
                    # TODO consider raising exception
                    ds.save()

        return report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['start_utc', 'hash', 'station']
