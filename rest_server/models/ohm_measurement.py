from django.db import models

from rest_server.models import Report
from rest_server.utils import model2str


class OhmHardwareInformation(models.Model):
    identifier = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)

    def __str__(self):
        return model2str(self)


class OhmSensorInformation(models.Model):
    identifier = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    hardware = models.ForeignKey(OhmHardwareInformation, on_delete=models.CASCADE)

    def __str__(self):
        # return model2str(self)
        return f'Sensor (id: {self.id}, name: "{self.name}", type: "{self.type}")'


class OhmSensorParameter(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    value = models.FloatField()
    default_value = models.FloatField()
    sensor = models.ForeignKey(OhmSensorInformation, on_delete=models.CASCADE)

    def __str__(self):
        return model2str(self)


class OhmSensorMeasurement(models.Model):
    timestamp = models.DateTimeField(help_text='Datetime of the measurement')
    value = models.FloatField()
    value_max = models.FloatField()
    value_min = models.FloatField()

    sensor = models.ForeignKey(OhmSensorInformation, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    def __str__(self):
        return model2str(self)
