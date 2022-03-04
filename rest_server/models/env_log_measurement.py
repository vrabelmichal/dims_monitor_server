from django.db import models

from rest_server.models.report import Report
from rest_server.models.station import Station
from rest_server.utils import model2str


class EnvironmentLogUpload(models.Model):
    captured_hour = models.DateTimeField(
        help_text='Datetime derived from the log file name (EnvData file).',
    )
    log_filename = models.CharField(
        max_length=260,
        help_text='Filename of a file on the remote station. ',
        null=True
    )
    # this might not be necessary !!
    is_historical = models.BooleanField(
        help_text='Indicates if file is being presently filled-in on the station'
    )

    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['report', 'captured_hour'], name='unique_pair_report_captured_hour'),
        ]

    def __str__(self):
        return model2str(self, None, ['captured_hour', 'station'])


class EnvironmentLogMeasurement(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['measurement_datetime', 'log_upload'], name='unique_pair_datetime_log_upload'),
            models.UniqueConstraint(fields=['measurement_datetime', 'station'], name='unique_pair_datetime_station'),
        ]

    measurement_datetime = models.DateTimeField(
        help_text='Datetime of the measurement.'
    )
    temperature_in = models.FloatField(
        help_text='Value of column "temperature_in" inside the Arduino data log file (EnvData). '
        'Unit: degrees of Celsius.',
    )
    temperature_out = models.FloatField(
        help_text='Value of column "temperature_out" inside the Arduino data log file (EnvData). '
        'Unit: degrees of Celsius.',
    )
    pressure_in = models.FloatField(
        help_text='Value of column "pressure_in" inside the Arduino data log file (EnvData). '
        'Unit: hPa.',
    )
    pressure_out = models.FloatField(
        help_text='Value of column "pressure_out" inside the Arduino data log file (EnvData). '
        'Unit: hPa.',
    )
    humidity_in = models.FloatField(
        help_text='Value of column "humidity_in" inside the Arduino data log file (EnvData). '
                  'Unit: Percent.',
    )
    humidity_out = models.FloatField(
        help_text='Value of column "humidity_out" inside the Arduino data log file (EnvData). '
                  'Unit: Percent.',
    )
    brightness = models.FloatField(
        help_text='Brightness from CdS sensor. '
                  'Value of column "brightness" inside the Arduino data log file (EnvData).',
    )
    fan1_rpm = models.FloatField(
        help_text='Value of column "fan1_rpm" inside the Arduino data log file (EnvData).',
    )
    fan2_rpm = models.FloatField(
        help_text='Value of column "fan2_rpm" inside the Arduino data log file (EnvData).',
    )
    fan1_pwm = models.FloatField(
        help_text='Value of column "fan1_pwm" inside the Arduino data log file (EnvData).',
    )
    fan2_pwm = models.FloatField(
        help_text='Value of column "fan2_pwm" inside the Arduino data log file (EnvData).',
    )

    log_upload = models.ForeignKey(EnvironmentLogUpload, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
