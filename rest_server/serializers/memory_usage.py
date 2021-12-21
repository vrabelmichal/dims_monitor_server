from rest_framework import serializers

from rest_server.models import MemoryUsage, Report


class MemoryUsageNestedSerializer(serializers.ModelSerializer):

    report = serializers.PrimaryKeyRelatedField(
        many=False, read_only=False, required=False,
        queryset=Report.objects.all()
    )

    class Meta:
        model = MemoryUsage
        fields = [
            'virtual_total',
            'virtual_available',
            'virtual_used',
            'virtual_free',
            'virtual_active',
            'virtual_inactive',
            'virtual_buffers',
            'virtual_cached',
            'virtual_shared',
            'virtual_slab',
            'virtual_wired',
            'swap_total',
            'swap_used',
            'swap_free',
            'swap_percent',
            'swap_sin',
            'swap_sout',
            'report'
        ]
