from rest_framework import serializers

from rest_server.models import Report, CameraStatus


class CameraStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraStatus
        fields = '__all__'


class CameraStatusNestedSerializer(serializers.ModelSerializer):

    # not required for validation
    # report is presumed to be already existing before the creation of cpu status
    report = serializers.PrimaryKeyRelatedField(
        many=False, read_only=False, required=False,
        queryset=Report.objects.all()
    )

    class Meta:
        model = CameraStatus
        fields = '__all__'

    def create(self, validated_data):

        if 'report' not in validated_data:
            raise RuntimeError('Field "report" is required for the creation')

        return CameraStatus.objects.create(**validated_data)
