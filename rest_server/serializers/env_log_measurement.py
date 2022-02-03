import datetime

from django.db import IntegrityError, transaction
from rest_framework import serializers

from rest_server.models import Report, Station, EnvironmentLogUpload, EnvironmentLogMeasurement


class EnvironmentLogUploadSerializer(serializers.Serializer):

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

    captured_hour = serializers.DateTimeField()
    is_historical = serializers.BooleanField()

    logfile = serializers.FileField(read_only=False, required=False)
    data = serializers.CharField(required=False)

    def create(self, validated_data):

        logfile = validated_data.pop('logfile', None)
        data = validated_data.pop('data', None)
        if data == '':
            data = None

        log_upload_create_dict = dict(validated_data)
        if logfile is not None:
            log_upload_create_dict['log_filename'] = logfile.name

        if data is None and logfile is None:
            raise RuntimeError('No data and no logfile were provided')
            #return None

        log_upload = EnvironmentLogUpload.objects.create(**log_upload_create_dict)

        parsed_data = None
        if logfile is None and data is not None:
            parsed_data = data.split('\n')
        elif logfile is not None:
            parsed_data = logfile

        if parsed_data:
            for line in parsed_data:
                line_str = line.decode() if isinstance(line, bytes) else line
                parsed_line = self.parse_env_log_line(line_str)
                parsed_line['station'] = validated_data['station']
                parsed_line['log_upload'] = log_upload

                # integrity error is possible if entry was included in a previous report
                try:
                    with transaction.atomic():
                        EnvironmentLogMeasurement.objects.create(**parsed_line)
                except IntegrityError as e:
                    pass
        return log_upload

    def parse_env_log_line(self, line):

        row = line.split(' ')

        # Row looks something like:
        # DATE TIME T= temp1 temp2 H= humidity1 humidity2 P= pressure1 pressure2 Br= brightness PWM= fan1 fan2 rpm= rmp1 rmp2
        # 2022/01/31 17:01:37 TX= 18.85 0.51 H= 41.77 0.00 P= 979.60 0.00 Br= 29.70 PWM= 0 0 rpm= 0 0

        date_str = row[0]
        time_str = row[1]

        datetime_obj = datetime.datetime.strptime(f'{date_str} {time_str}', '%Y/%m/%d %H:%M:%S')

        ofst = 2

        temp1 = float(row[ofst + 1])
        temp2 = float(row[ofst + 2])

        hum1 = float(row[ofst + 4])
        hum2 = float(row[ofst + 5])

        press1 = float(row[ofst + 7])
        press2 = float(row[ofst + 8])

        bright = float(row[ofst + 10])

        pwm1 = float(row[ofst + 12])
        pwm2 = float(row[ofst + 13])

        rpm1 = float(row[ofst + 15])
        rpm2 = float(row[ofst + 16])

        return dict(
            measurement_datetime=datetime_obj,
            temperature_in=temp1,
            temperature_out=temp2,
            humidity_in=hum1,
            humidity_out=hum2,
            pressure_in=press1,
            pressure_out=press2,
            brightness=bright,
            fan1_pwm=pwm1,
            fan2_pwm=pwm2,
            fan1_rpm=rpm1,
            fan2_rpm=rpm2
        )
