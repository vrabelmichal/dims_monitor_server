from rest_framework import serializers

from rest_server.models import Report
from rest_server.models.cpu_status import CpuStatus


class CpuStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CpuStatus
        fields = '__all__'


class CpuStatusNestedSerializer(serializers.ModelSerializer):

    # not required for validation
    # report is presumed to be already existing before the creation of disk usage

    report = serializers.PrimaryKeyRelatedField(
        many=False, read_only=False, required=False,
        queryset=Report.objects.all()
    )


    class Meta:
        model = CpuStatus
        fields = '__all__'

    def create(self, validated_data):

        if 'report' not in validated_data:
            raise RuntimeError('Field "report" is required for the creation')

        return CpuStatus.objects.create( **validated_data)
