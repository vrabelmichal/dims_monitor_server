from rest_framework import serializers

from rest_server.models import Report
from rest_server.serializers.cpu_status import CpuStatusNestedSerializer
from rest_server.serializers.disk_usage import DiskUsageNestedSerializer


# TODO move this into a configuration file
ACQUIRED_MODULES = ['disk_usage', 'cpu_status']

MODULE_SERIALIZER_MAPPING = dict(
    disk_usage=DiskUsageNestedSerializer,
    cpu_status=CpuStatusNestedSerializer
)


class ReportNestedSerializer(serializers.ModelSerializer):

    disk_usage = DiskUsageNestedSerializer(many=True, read_only=False, required=False)  # intentionally singular
    cpu_status = CpuStatusNestedSerializer(many=True, read_only=False, required=False)  # intentionally singular

    class Meta:
        model = Report
        fields = [
            'start_utc', 'hash', 'station',
            'disk_usage', 'cpu_status'
        ]

    def create(self, validated_data):

        module_data_dict = dict()

        for module_name in ACQUIRED_MODULES:
            if module_name in validated_data:
                module_data_dict[module_name] = validated_data.pop(module_name)

        report = Report.objects.create(**validated_data)

        for module_name, module_data in module_data_dict.items():
            if not isinstance(module_data, (list, tuple)):
                module_data = [module_data]

            for module_data_entry in module_data:
                module_data_entry['report'] = report.id
                ds = MODULE_SERIALIZER_MAPPING[module_name](data=module_data_entry)
                if ds.is_valid():
                    ds.save()

        return report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['start_utc', 'hash', 'station']
