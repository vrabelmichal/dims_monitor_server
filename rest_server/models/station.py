from django.db import models

from rest_server.models.observing_station import ObservingStation


class Station(models.Model):
    """
    This model class should be renamed to "Device", but for backward compatibility the name is kept
    """
    name = models.CharField(max_length=50, unique=True)
    priority = models.IntegerField(default=0)
    observing_station = models.ForeignKey(ObservingStation, on_delete=models.RESTRICT, null=True)
    camera = models.CharField(max_length=50, null=True, blank=True)
    type = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'Reporting device (station) "{self.name}"'

    class Meta:
        indexes = [
            models.Index(fields=['type']),
            models.Index(fields=['camera']),
        ]