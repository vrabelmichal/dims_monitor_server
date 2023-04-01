from django.db import models


class ObservingStation(models.Model):
    """
    This model class should be renamed to "Device", but for backward compatibility the name is kept
    """
    name = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=50, unique=True)
    priority = models.IntegerField(default=0)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    altitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'Observing station "{self.label}" ("{self.name}")'

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['label']),
            models.Index(fields=['-priority']),
        ]
