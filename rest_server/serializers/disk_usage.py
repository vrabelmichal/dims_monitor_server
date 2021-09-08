from rest_framework import serializers

from rest_server.models import DiskPartition, DiskUsage, Report


class DiskPartitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiskPartition
        fields = ['device', 'mountpoint', 'fstype', 'opts']


class DiskUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiskUsage
        fields = ['disk_partition', 'total', 'used', 'free', 'report']


class DiskUsageNestedSerializer(serializers.ModelSerializer):

    disk_partition = DiskPartitionSerializer(many=False, read_only=False)

    # not required for validation
    # report is presumed to be already existing before the creation of disk usage

    report = serializers.PrimaryKeyRelatedField(
        many=False, read_only=False, required=False,
        queryset=Report.objects.all()
    )

    class Meta:
        model = DiskUsage
        fields = ['disk_partition', 'total', 'used', 'free', 'report']

    def create(self, validated_data):
        disk_partition_data = validated_data.pop('disk_partition')
        disk_partition, created = DiskPartition.objects.get_or_create(**disk_partition_data)
        if 'report' not in validated_data:
            raise RuntimeError('Field "report" is required for the creation')

        return DiskUsage.objects.create(disk_partition=disk_partition, **validated_data)

        # report_data = validated_data.pop('report')
        # report, created = Report.objects.get_or_create(**report_data)
        # return DiskUsage.objects.create(disk_partition=disk_partition, report=report, **validated_data)