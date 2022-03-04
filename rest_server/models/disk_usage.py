from django.db import models

from rest_server.models import Report
from rest_server.utils import model2str


class DiskPartition(models.Model):
    device = models.CharField(max_length=25)
    mountpoint = models.CharField(max_length=255)
    fstype = models.CharField(max_length=25)
    opts = models.CharField(max_length=255)

    def __str__(self):
        # return model2str(self, fields=('mountpoint', ))
        model_name = self.__class__.__name__
        fields_list = ['device']
        if self.device != self.mountpoint:
            fields_list.append('mountpoint')
        fields_str = ', '.join([f'{n}: {getattr(self, n)}' for n in fields_list])
        return f'{model_name} ({fields_str})'


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
