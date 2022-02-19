from django.db import models

from rest_server.models import Report
from rest_server.utils import model2str


class CpuStatus(models.Model):
    cpu_id = models.CharField(default='all', max_length=15,
                              verbose_name='Unique identifier of a CPU ("all" for measurements across all CPUs)')

    cpu_freq_mean = models.FloatField(verbose_name='Mean CPU Frequency')
    cpu_freq_min = models.FloatField(verbose_name='Minimum CPU Frequency')
    cpu_freq_max = models.FloatField(verbose_name='Maximum CPU Frequency')

    cpu_time_percent_user_mean = models.FloatField(help_text='Mean utilization percentage for "user" CPU time')
    cpu_time_percent_system_mean = models.FloatField(help_text='Mean utilization percentage for "system" CPU time')
    cpu_time_percent_idle_mean = models.FloatField(help_text='Mean utilization percentage for "idle" CPU time')
    cpu_time_percent_nice_mean = models.FloatField(help_text='Mean utilization percentage for "nice" CPU time (Linux)')
    cpu_time_percent_iowait_mean = models.FloatField(help_text='Mean utilization percentage for "iowait" CPU time (Linux)')
    cpu_time_percent_irq_mean = models.FloatField(help_text='Mean utilization percentage for "irq" CPU time (Linux)')
    cpu_time_percent_softirq_mean = models.FloatField(help_text='Mean utilization percentage for "softirq" CPU time (Linux)')
    cpu_time_percent_steal_mean = models.FloatField(help_text='Mean utilization percentage for "steal" CPU time (Linux)')
    cpu_time_percent_guest_mean = models.FloatField(help_text='Mean utilization percentage for "guest" CPU time (Linux)')
    cpu_time_percent_guest_nice_mean = models.FloatField(help_text='Mean utilization percentage for "guest_nice" CPU time (Linux)')
    cpu_time_percent_interrupt_mean = models.FloatField(help_text='Mean utilization percentage for "interrupt" CPU time (Windows)')
    cpu_time_percent_dpc_mean = models.FloatField(help_text='Mean utilization percentage for "dpc" CPU time (Windows)')

    cpu_time_percent_user_max = models.FloatField(help_text='Max utilization percentage for "user" CPU time')
    cpu_time_percent_system_max = models.FloatField(help_text='Max utilization percentage for "system" CPU time')
    cpu_time_percent_idle_max = models.FloatField(help_text='Max utilization percentage for "idle" CPU time')
    cpu_time_percent_nice_max = models.FloatField(help_text='Max utilization percentage for "nice" CPU time (Linux)')
    cpu_time_percent_iowait_max = models.FloatField(help_text='Max utilization percentage for "iowait" CPU time (Linux)')
    cpu_time_percent_irq_max = models.FloatField(help_text='Max utilization percentage for "irq" CPU time (Linux)')
    cpu_time_percent_softirq_max = models.FloatField(help_text='Max utilization percentage for "softirq" CPU time (Linux)')
    cpu_time_percent_steal_max = models.FloatField(help_text='Max utilization percentage for "steal" CPU time (Linux)')
    cpu_time_percent_guest_max = models.FloatField(help_text='Max utilization percentage for "guest" CPU time (Linux)')
    cpu_time_percent_guest_nice_max = models.FloatField(help_text='Max utilization percentage for "guest_nice" CPU time (Linux)')
    cpu_time_percent_interrupt_max = models.FloatField(help_text='Max utilization percentage for "interrupt" CPU time (Windows)')
    cpu_time_percent_dpc_max = models.FloatField(help_text='Max utilization percentage for "dpc" CPU time (Windows)')

    cpu_time_percent_user_min = models.FloatField(help_text='Min utilization percentage for "user" CPU time')
    cpu_time_percent_system_min = models.FloatField(help_text='Min utilization percentage for "system" CPU time')
    cpu_time_percent_idle_min = models.FloatField(help_text='Min utilization percentage for "idle" CPU time')
    cpu_time_percent_nice_min = models.FloatField(help_text='Min utilization percentage for "nice" CPU time (Linux)')
    cpu_time_percent_iowait_min = models.FloatField(help_text='Min utilization percentage for "iowait" CPU time (Linux)')
    cpu_time_percent_irq_min = models.FloatField(help_text='Min utilization percentage for "irq" CPU time (Linux)')
    cpu_time_percent_softirq_min = models.FloatField(help_text='Min utilization percentage for "softirq" CPU time (Linux)')
    cpu_time_percent_steal_min = models.FloatField(help_text='Min utilization percentage for "steal" CPU time (Linux)')
    cpu_time_percent_guest_min = models.FloatField(help_text='Min utilization percentage for "guest" CPU time (Linux)')
    cpu_time_percent_guest_nice_min = models.FloatField(help_text='Min utilization percentage for "guest_nice" CPU time (Linux)')
    cpu_time_percent_interrupt_min = models.FloatField(help_text='Max utilization percentage for "interrupt" CPU time (Windows)')
    cpu_time_percent_dpc_min = models.FloatField(help_text='Max utilization percentage for "dpc" CPU time (Windows)')

    cpu_time_user = models.FloatField(help_text='Time spent by normal processes executing in user mode (user);'
                                                ' on Linux this also includes guest time')
    cpu_time_system = models.FloatField(help_text='Time spent by processes executing in kernel mode (system)')
    cpu_time_idle = models.FloatField(help_text='Time spent doing nothing (idle)')
    cpu_time_nice = models.FloatField(help_text='Time spent by niced (prioritized) processes executing in user mode (UNIX);'
                                                ' on Linux this also includes guest_nice time')
    cpu_time_iowait = models.FloatField(help_text='Time spent waiting for I/O to complete. This is not accounted in idle time counter (Linux)')
    cpu_time_irq = models.FloatField(help_text='Time spent for servicing hardware interrupts (Linux, BSD)')
    cpu_time_softirq = models.FloatField(help_text='Time spent for servicing software interrupts (Linux)')
    cpu_time_steal = models.FloatField(help_text='Time spent by other operating systems running in a virtualized environment (Linux)')
    cpu_time_guest = models.FloatField(help_text='Time spent running a virtual CPU for guest operating systems under the control of the Linux kernel (Linux)')
    cpu_time_guest_nice = models.FloatField(help_text='Time spent running a niced guest (Linux)')
    cpu_time_interrupt = models.FloatField(help_text='Time spent for servicing hardware interrupts (Windows)')
    cpu_time_dpc = models.FloatField(help_text='Time spent servicing deferred procedure calls (DPCs) (Windows);'
                                                   ' DPCs are interrupts that run at a lower priority than standard interrupts.')

    load_avg_1min = models.FloatField(help_text='The average system load over the last 1 min')
    load_avg_5min = models.FloatField(help_text='The average system load over the last 5 min')
    load_avg_15min = models.FloatField(help_text='The average system load over the last 15 min')

    load_avg_percent_1min = models.FloatField(help_text='The average system load over the last 1 min in percent')
    load_avg_percent_5min = models.FloatField(help_text='The average system load over the last 5 min in percent')
    load_avg_percent_15min = models.FloatField(help_text='The average system load over the last 15 min in percent')

    cpu_stat_ctx_switches = models.FloatField(help_text='Number of context switches (voluntary + involuntary) since boot.')
    cpu_stat_interrupts = models.FloatField(help_text='Number of interrupts since boot.')
    cpu_stat_soft_interrupts = models.FloatField(help_text='Nnumber of software interrupts since boot. Always set to 0 on Windows and SunOS.')
    cpu_stat_syscalls = models.FloatField(help_text='Number of system calls since boot. Always set to 0 on Linux.')

    cpu_percent_min = models.FloatField(help_text='Mean system-wide CPU utilization as a percentage')
    cpu_percent_max = models.FloatField(help_text='Maximum system-wide CPU utilization as a percentage')
    cpu_percent_mean = models.FloatField(help_text='Minimum system-wide CPU utilization as a percentage')

    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    def __str__(self):
        return model2str(self, fields=['cpu_id', 'cpu_freq_mean', 'load_avg_percent_5min'])