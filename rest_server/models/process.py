from django.db import models

from rest_server.models import Report
from rest_server.utils import model2str


class Process(models.Model):
    name = models.CharField(
        max_length=255, null=True, blank=True,
        help_text='The process name. On Windows the return value is cached after first call. '
        'Not on POSIX because the process name may change.'
    )
    pid = models.IntegerField(help_text='Process PID')
    ppid = models.IntegerField(help_text='Parent process PID')
    exe = models.CharField(
        max_length=255, null=True, blank=True,
        help_text='The process executable as an absolute path. On some systems this may also be an empty string. '
        'The return value is cached after first call.'
    )
    cmdline = models.CharField(
        max_length=4096, null=True, blank=True,
        help_text='The command line this process has been called with as a list of strings. '
    )
    cwd = models.CharField(
        max_length=4096, null=True, blank=True,
        help_text='The process current working directory as an absolute path.'
    )
    username = models.CharField(
        max_length=64, null=True, blank=True,
        help_text='The name of the user that owns the process. '
                  'On UNIX this is calculated by using real process uid.'
    )
    create_time = models.FloatField(
        help_text='The process creation time as a floating point number expressed in seconds since the epoch.'
    )
    cpu_percent = models.FloatField(
        help_text='A float representing the process CPU utilization as a percentage '
                  'which can also be > 100.0 in case of a process running multiple threads on different CPUs. '
                  'See: https://psutil.readthedocs.io/en/latest/#psutil.Process.cpu_percent'
    )
    memory_info_rss = models.IntegerField(
        verbose_name='Resident Set Size',
        help_text='The non-swapped physical memory a process has used.'
    )
    memory_info_vms = models.IntegerField(
        verbose_name='Virtual Memory Size',
        help_text='The total amount of virtual memory used by the process.'
    )

    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    def __str__(self):
        return model2str(self, fields=['exe', 'pid', 'username'])
