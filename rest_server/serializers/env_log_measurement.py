import datetime
import logging

import pytz
from django.db import IntegrityError, transaction
from rest_framework import serializers

from rest_server.models import Report, Station, EnvironmentLogUpload, EnvironmentLogMeasurement, EnvironmentLogType


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

    logfile = serializers.FileField(read_only=False, allow_empty_file=True, required=False)
    data = serializers.CharField(required=False, allow_blank=True)

    log_filename = serializers.CharField(required=False, allow_blank=True, default='')

    data_timezone = serializers.CharField(required=False, default='utc')
    type = serializers.CharField(required=False, default='common')


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._logger = logging.getLogger('rest_server.EnvironmentLogUploadSerializer')

    def create(self, validated_data):

        logfile = validated_data.pop('logfile', None)
        data = validated_data.pop('data', None)
        if data == '':
            data = None

        data_timezone_str = validated_data.pop('data_timezone', 'utc')
        data_tzinfo = pytz.timezone(data_timezone_str)

        env_log_type = validated_data.pop('type', 'common')

        log_upload_create_dict = dict(validated_data)
        if logfile is not None:
            log_upload_create_dict['log_filename'] = logfile.name

        if data is None and logfile is None:
            raise RuntimeError('No data and no logfile were provided')
            #return None

        type, type_created = EnvironmentLogType.objects.get_or_create(name=env_log_type)
        log_upload_create_dict['type'] = type

        log_upload = EnvironmentLogUpload.objects.create(**log_upload_create_dict)

        parsed_data = None
        if logfile is None and data is not None:
            parsed_data = data.split('\n')
        elif logfile is not None:
            parsed_data = logfile

        if parsed_data:

            parsing_errors_list = []

            for line in parsed_data:
                line_str = line.decode() if isinstance(line, bytes) else line
                line_str = line_str.strip()
                parsed_line = None
                if len(line_str):
                    try:
                        parsed_line = self.parse_env_log_line(line_str, tzinfo=data_tzinfo)
                    except Exception as e:
                        if len(parsing_errors_list) < 5:
                            parsing_errors_list.append(e)

                    if len(parsing_errors_list) > 0:
                        self._logger.warning(
                            'Data parsing errors caught, up to first five errors are being listed:\n'
                            + "\n".join([str(e) for e in parsing_errors_list])
                        )

                if parsed_line is not None:
                    parsed_line['station'] = validated_data['station']
                    parsed_line['log_upload'] = log_upload

                    # integrity error is possible if entry was included in a previous report
                    try:
                        with transaction.atomic():
                            EnvironmentLogMeasurement.objects.create(**parsed_line)
                    except IntegrityError as e:
                        pass

        return log_upload

    def _sanitize_val(self, val):
        val = val.replace('\0', '').strip()
        return val

    def parse_env_log_line(self, line, tzinfo=pytz.UTC, is_dst=False):

        # try:

        row = line.split(' ')

        if len(row) < 19:
            raise ValueError(f'Line has to few columns (19 expected, {len(row)} available)')

        # Row looks something like:
        # DATE TIME T= temp1 temp2 H= humidity1 humidity2 P= pressure1 pressure2 Br= brightness PWM= fan1 fan2 rpm= rmp1 rmp2
        # 2022/01/31 17:01:37 TX= 18.85 0.51 H= 41.77 0.00 P= 979.60 0.00 Br= 29.70 PWM= 0 0 rpm= 0 0

        date_str = self._sanitize_val(row[0])
        time_str = self._sanitize_val(row[1])
        datetime_obj = datetime.datetime.strptime(f'{date_str} {time_str}', '%Y/%m/%d %H:%M:%S')
        datetime_obj = tzinfo.localize(datetime_obj, is_dst=is_dst)
        datetime_obj = datetime_obj.astimezone(pytz.UTC)

        ofst = 2

        # Degree Celsius
        temp1 = float(self._sanitize_val(row[ofst + 1]))
        temp2 = float(self._sanitize_val(row[ofst + 2]))

        # Percent
        hum1 = float(self._sanitize_val(row[ofst + 4]))
        hum2 = float(self._sanitize_val(row[ofst + 5]))

        # hPa
        press1 = float(self._sanitize_val(row[ofst + 7]))
        press2 = float(self._sanitize_val(row[ofst + 8]))

        # Brightness from CdS sensor, range: 0-102.3
        # Min = 0 (dark), Max = 255 (dark)
        bright = float(self._sanitize_val(row[ofst + 10]))

        pwm1 = float(self._sanitize_val(row[ofst + 12]))
        pwm2 = float(self._sanitize_val(row[ofst + 13]))

        rpm1 = float(self._sanitize_val(row[ofst + 15]))
        rpm2 = float(self._sanitize_val(row[ofst + 16]))

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

        # except Exception as e:
        #     print(e)

