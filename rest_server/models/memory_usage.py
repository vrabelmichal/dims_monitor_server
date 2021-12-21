from django.db import models

from rest_server.models import Report
from rest_server.utils import model2str


class MemoryUsage(models.Model):
    virtual_total = models.BigIntegerField(help_text='total physical memory (exclusive swap)')
    virtual_available = models.BigIntegerField(help_text='the memory that can be given instantly to processes without the system going into swap')
    virtual_used = models.BigIntegerField(help_text='memory used, calculated differently depending on the platform and designed for informational purposes only. total - free does not necessarily match used.')  #
    virtual_free = models.BigIntegerField(help_text='memory not being used at all (zeroed) that is readily available; note that this doesn’t reflect the actual memory available (use available instead). total - used does not necessarily match free.')  #
    virtual_active = models.BigIntegerField(default=-1, help_text='(UNIX): memory currently in use or very recently used, and so it is in RAM.')  #
    virtual_inactive = models.BigIntegerField(default=-1, help_text='(UNIX): memory that is marked as not used.')  #
    virtual_buffers = models.BigIntegerField(default=-1, help_text='(Linux, BSD): cache for things like file system metadata.')  #
    virtual_cached = models.BigIntegerField(default=-1, help_text='(Linux, BSD): cache for various things.')  #
    virtual_shared = models.BigIntegerField(default=-1, help_text='(Linux, BSD): memory that may be simultaneously accessed by multiple processes.')  #
    virtual_slab = models.BigIntegerField(default=-1, help_text='(Linux): in-kernel data structures cache.')  #
    virtual_wired = models.BigIntegerField(default=-1, help_text='(BSD, macOS): memory that is marked to always stay in RAM. It is never moved to disk.')  #

    swap_total = models.BigIntegerField(help_text='total swap memory in bytes')  #
    swap_used = models.BigIntegerField(help_text='used swap memory in bytes')  #
    swap_free = models.BigIntegerField(help_text='free swap memory in bytes')  #
    swap_percent = models.FloatField(help_text='the percentage usage calculated as (total - available) / total * 100')  #
    swap_sin = models.BigIntegerField(help_text='the number of bytes the system has swapped in from disk (cumulative)')  #
    swap_sout = models.BigIntegerField(help_text='the number of bytes the system has swapped out from disk (cumulative)')  #

    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    def __str__(self):
        model_name = self.__class__.__name__
        field_value_strs = []

        for field in ['virtual_used', 'virtual_free', 'swap_used', 'swap_free']:
            v = getattr(self, field.name)
            v_str = f'"{v}"' if isinstance(v, str) else v
            field_value_strs.append(f'{field.name}: {v_str}')

        return f'{model_name} ({", ".join(field_value_strs)})'