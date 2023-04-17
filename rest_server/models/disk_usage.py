from django.db import models

from rest_server.models.disk_partition import DiskPartition
from rest_server.models.report import Report
from rest_server.utils import model2str

class DiskUsage(models.Model):
    class Meta:
        verbose_name_plural = "disk usage records"

    disk_partition = models.ForeignKey(DiskPartition, on_delete=models.CASCADE)
    total = models.BigIntegerField()
    used = models.BigIntegerField()
    free = models.BigIntegerField()

    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    def get_percent(self):
        return self.used / self.total

    def __str__(self):
        return model2str(self, fields=('disk_partition', 'used', ))
