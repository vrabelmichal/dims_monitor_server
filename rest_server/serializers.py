from rest_framework import serializers

from rest_server.models import HddPartition, DiskUsage


class HddPartitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HddPartition
        fields = ['device', 'mountpoint', 'fstype', 'opts']


class DiskUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiskUsage
        fields = ['hdd_partition', 'total', 'used', 'free']