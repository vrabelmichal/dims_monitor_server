from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from rest_server.models import Report, \
    OhmHardwareInformation, OhmSensorInformation, OhmSensorParameter, OhmSensorMeasurement


class OhmHardwareInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OhmHardwareInformation
        fields = ['identifier', 'name', 'type']


class OhmSensorParameterPartialSerializer(serializers.ModelSerializer):
    class Meta:
        model = OhmSensorParameter
        fields = ['name', 'description', 'value', 'default_value'] # sensor


class OhmSensorInformationNestedSerializer(serializers.ModelSerializer):
    hardware = OhmHardwareInformationSerializer(many=False, read_only=False)
    parameters = OhmSensorParameterPartialSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = OhmSensorInformation
        fields = ['identifier', 'name', 'type', 'hardware', 'parameters']

    def create(self, validated_data):
        hardware_data = validated_data.pop('hardware')
        parameters_data = validated_data.pop('parameters')  # list?

        hardware, hardware_created = OhmHardwareInformation.objects.get_or_create(**hardware_data)

        # get_or_create or create ?
        sensor, sensor_created = OhmSensorInformation.objects.get_or_create(
            hardware=hardware, **validated_data
        )

        for parameter_data in parameters_data:
            parameter, parameter_created = OhmSensorParameter.objects.get_or_create(
                sensor=sensor, **parameter_data
            )

        return sensor


class OhmSensorMeasurementNestedSerializer(serializers.ModelSerializer):

    sensor = OhmSensorInformationNestedSerializer(many=False, read_only=False)

    # not required for validation
    # report is presumed to be already existing before the creation of disk usage

    report = serializers.PrimaryKeyRelatedField(
        many=False, read_only=False, required=False,
        queryset=Report.objects.all()
    )

    class Meta:
        model = OhmSensorMeasurement
        fields = ['timestamp', 'value', 'value_max', 'value_min',
                  'sensor', 'report']

    def create(self, validated_data):
        sensor_data = validated_data.pop('sensor')

        sensor_data_serializer = OhmSensorInformationNestedSerializer(data=sensor_data)
        sensor_data_serializer.is_valid(raise_exception=True)

        sensor = sensor_data_serializer.save()

        if 'report' not in validated_data:
            raise ValidationError('Field "report" is required for the creation')

        return OhmSensorMeasurement.objects.create(
            sensor=sensor, **validated_data)

        # report_data = validated_data.pop('report')
        # report, created = Report.objects.get_or_create(**report_data)
        # return DiskUsage.objects.create(disk_partition=disk_partition, report=report, **validated_data)