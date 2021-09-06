from rest_framework import serializers

from rest_server.models import DiskPartition, DiskUsage, Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['start_utc', 'hash']


class DiskPartitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiskPartition
        fields = ['device', 'mountpoint', 'fstype', 'opts']


class DiskUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiskUsage
        fields = ['hdd_partition', 'total', 'used', 'free', 'report']


class DiskUsageNestedSerializer(serializers.ModelSerializer):

    disk_partition = DiskPartitionSerializer(many=False, read_only=False)

    class Meta:
        model = DiskUsage
        fields = ['disk_partition', 'total', 'used', 'free', 'report']

    def create(self, validated_data):
        disk_partition_data = validated_data.pop('disk_partition')
        disk_partition = DiskPartition.objects.get_or_create(**disk_partition_data)
        return DiskUsage.objects.create(disk_partition=disk_partition, **validated_data)


class ReportNestedSerializer(serializers.ModelSerializer):

    disk_usage = DiskUsageSerializer(many=True, read_only=False)  # intentionally singular

    class Meta:
        model = Report
        fields = [
            'start_utc', 'hash', 'station',
            'disk_usage'
        ]

    def create(self, validated_data):
        disk_usages_data = validated_data.pop('disk_usage')
        report = Report.objects.get_or_create(**validated_data)
        for disk_usage_data in disk_usages_data:
            ds = DiskUsageSerializer(data=disk_usage_data) # this might not work
            if ds.is_valid():
                ds.save()
        return report