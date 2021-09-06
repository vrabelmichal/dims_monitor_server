from django.db import models


class HddPartition(models.Model):
    device = models.CharField(max_length=25)
    mountpoint = models.CharField(max_length=255)
    fstype = models.CharField(max_length=25)
    opts = models.CharField(max_length=255)


class DiskUsage(models.Model):
    hdd_partition = models.ForeignKey(HddPartition, on_delete=models.CASCADE)
    total = models.PositiveBigIntegerField()
    used = models.PositiveBigIntegerField()
    free = models.PositiveBigIntegerField()

    report = models.ForeignKey(Report)

    def get_percent(self):
        return self.used / self.total


class Report(models.Model):
    start_utc = models.DateTimeField()
    hash = models.BigIntegerField()
