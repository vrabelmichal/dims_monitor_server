from django.db import models

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