from django.db import models


def model2str(model, model_name=None):
    if model_name is None:
        model_name = model.__class__.__name__
    field_value_strs = []

    for field in model._meta.fields:
        v = getattr(model, field.name)
        v_str = f'"{v}"' if isinstance(v, str) else v
        field_value_strs.append(f'{field.name}: {v_str}')

    return f'{model_name} ({", ".join(field_value_strs)})'


class Report(models.Model):
    start_utc = models.DateTimeField()
    station = models.CharField(max_length=50, default='dims_0')  # default is just temporary, should be done by authentification&authorization
    # station = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    hash = models.BigIntegerField()

    def __str__(self):
        return (f'Station status report '
                f'(station: "{self.station}", measurement started at: {self.start_utc}, data hash: {self.hash})')


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
