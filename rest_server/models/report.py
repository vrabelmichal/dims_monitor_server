from django.db import models

from rest_server.models.station import Station


class Report(models.Model):
    start_utc = models.DateTimeField()
    post_utc = models.DateTimeField()
    retrieved_utc = models.DateTimeField()
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    hash = models.BigIntegerField(unique=True)
    fully_processed = models.BooleanField(default=False)
    integrity_errors = models.JSONField(null=True)

    def __str__(self):
        return (f'Station status report '
                f'(station: "{self.station.name}", measurement started at: {self.start_utc}, data hash: {self.hash})')
