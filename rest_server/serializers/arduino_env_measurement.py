from rest_framework import serializers

from rest_server.models import Report, UfoCaptureOutputEntry, Station


class ArduinoLogUploadSerializer(serializers.ModelSerializer):

    # not required for validation
    # report is presumed to be already existing before the creation of ufo capture output entry
    # read_only=False is necessary for values to be available in validated_data parameter of `create(...)` method

    report = serializers.PrimaryKeyRelatedField(
        many=False, read_only=False, required=False,
        queryset=Report.objects.all()
    )

    station = serializers.PrimaryKeyRelatedField(
        many=False, read_only=False, required=False,
        queryset=Station.objects.all()
    )

    class Meta:
        model = UfoCaptureOutputEntry
        fields = '__all__'

    def create(self, validated_data):

        return None

        # if 'report' not in validated_data:
        #     raise RuntimeError('Field "report" is required for the creation')
        #
        # return UfoCaptureOutputEntry.objects.create(
        #     **validated_data
        # )

