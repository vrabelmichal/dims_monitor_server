from django.db import models


class Station(models.Model):
    name = models.CharField(max_length=50, unique=True)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return f'Station "{self.name}"'
