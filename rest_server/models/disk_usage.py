from django.db import models

from rest_server.models import Report
from rest_server.utils import model2str


class DiskPartition(models.Model):
    device = models.CharField(max_length=25)
    mountpoint = models.CharField(max_length=255)
    fstype = models.CharField(max_length=25)
    opts = models.CharField(max_length=255)

    def __str__(self):
        return model2str(self)


class DiskUsage(models.Model):
    disk_partition = models.ForeignKey(DiskPartition, on_delete=models.CASCADE)
    total = models.PositiveBigIntegerField()
    used = models.PositiveBigIntegerField()
    free = models.PositiveBigIntegerField()

    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    def get_percent(self):
        return self.used / self.total

    def __str__(self):
        return model2str(self)