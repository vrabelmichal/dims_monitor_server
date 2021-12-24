from django.db import models


class Report(models.Model):
    start_utc = models.DateTimeField()
    retrieved_utc = models.DateTimeField()
    station = models.CharField(max_length=50, default='dims_0')  # default is just temporary, should be done by authentification&authorization
    # station = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    hash = models.BigIntegerField(unique=True)

    def __str__(self):
        return (f'Station status report '
                f'(station: "{self.station}", measurement started at: {self.start_utc}, data hash: {self.hash})')