from django.db import models

from rest_server.models import Report
from rest_server.utils import model2str


class CameraStatus(models.Model):
    class Meta:
        verbose_name_plural = "Camera status records"

    gain = models.FloatField(
        help_text='Camera gain setting',
        null=True, blank=True
    )
    iris = models.FloatField(
        help_text='Camera iris setting. For ONVIF, this might be a derived value.',
        null=True, blank=True
    )
    iris_raw = models.FloatField(
        help_text='Camera iris_raw setting (ONVIF)',
        null=True, blank=True
    )
    one_over_shutter_speed = models.FloatField(
        help_text='Camera shutter speed setting. For ONVIF, this might be a derived value.',
        null=True, blank=True
    )
    exposure_time = models.FloatField(
        help_text='Camera exposure time setting. Provided through ONVIF by default.',
        null=True, blank=True
    )
    gamma = models.CharField(
        max_length=32, help_text='Camera gamma setting',
        null=True, blank=True
    )

    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    def __str__(self):
        return model2str(self, fields=['gain','iris','one_over_shutter_speed','gamma',])
