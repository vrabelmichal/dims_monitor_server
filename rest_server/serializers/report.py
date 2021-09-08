from rest_framework import serializers

from rest_server.models import Report
from rest_server.serializers.disk_usage import DiskUsageNestedSerializer


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['start_utc', 'hash', 'station']


class ReportNestedSerializer(serializers.ModelSerializer):

    disk_usage = DiskUsageNestedSerializer(many=True, read_only=False)  # intentionally singular

    class Meta:
        model = Report
        fields = [
            'start_utc', 'hash', 'station',
            'disk_usage'
        ]

    def create(self, validated_data):
        disk_usages_data = validated_data.pop('disk_usage')
        report = Report.objects.create(**validated_data)  # TODO get_or_create
        for disk_usage_data in disk_usages_data:
            # disk_usage_data['report'] = report  # this might be incorrect
            disk_usage_data['report'] = report.id
            ds = DiskUsageNestedSerializer(data=disk_usage_data)  # this might not work
            if ds.is_valid():
                ds.save()
        return report