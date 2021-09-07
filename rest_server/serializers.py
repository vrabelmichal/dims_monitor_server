from rest_framework import serializers

from rest_server.models import DiskPartition, DiskUsage, Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['start_utc', 'hash', 'station']


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

    # not required for validation
    # report is presumed to be already existing before the creation of disk usage
    # report = ReportSerializer(many=False, read_only=False, required=False)

    report = serializers.PrimaryKeyRelatedField(
        many=False, read_only=False, required=False,
        queryset=Report.objects.all()
    )

    class Meta:
        model = DiskUsage
        fields = ['disk_partition', 'total', 'used', 'free', 'report']
        # fields = ['disk_partition', 'total', 'used', 'free']
        # 'report' intentionally not included, otherwise ReportNestedSerializer().is_valid() fails

    def create(self, validated_data):
        disk_partition_data = validated_data.pop('disk_partition')
        disk_partition, created = DiskPartition.objects.get_or_create(**disk_partition_data)
        if 'report' not in validated_data:
            raise RuntimeError('Field "report" is required for the creation')

        return DiskUsage.objects.create(disk_partition=disk_partition, **validated_data)

        # report_data = validated_data.pop('report')
        # report, created = Report.objects.get_or_create(**report_data)
        # return DiskUsage.objects.create(disk_partition=disk_partition, report=report, **validated_data)


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