# Generated by Django 3.2.7 on 2021-10-21 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rest_server', '0014_delete_memoryusage'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemoryUsage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('virtual_total', models.PositiveBigIntegerField(help_text='total physical memory (exclusive swap)')),
                ('virtual_available', models.PositiveBigIntegerField(help_text='the memory that can be given instantly to processes without the system going into swap')),
                ('virtual_used', models.PositiveBigIntegerField(help_text='memory used, calculated differently depending on the platform and designed for informational purposes only. total - free does not necessarily match used.')),
                ('virtual_free', models.PositiveBigIntegerField(help_text='memory not being used at all (zeroed) that is readily available; note that this doesn’t reflect the actual memory available (use available instead). total - used does not necessarily match free.')),
                ('virtual_active', models.PositiveBigIntegerField(default=-1, help_text='(UNIX): memory currently in use or very recently used, and so it is in RAM.')),
                ('virtual_inactive', models.PositiveBigIntegerField(default=-1, help_text='(UNIX): memory that is marked as not used.')),
                ('virtual_buffers', models.PositiveBigIntegerField(default=-1, help_text='(Linux, BSD): cache for things like file system metadata.')),
                ('virtual_cached', models.PositiveBigIntegerField(default=-1, help_text='(Linux, BSD): cache for various things.')),
                ('virtual_shared', models.PositiveBigIntegerField(default=-1, help_text='(Linux, BSD): memory that may be simultaneously accessed by multiple processes.')),
                ('virtual_slab', models.PositiveBigIntegerField(default=-1, help_text='(Linux): in-kernel data structures cache.')),
                ('virtual_wired', models.PositiveBigIntegerField(default=-1, help_text='(BSD, macOS): memory that is marked to always stay in RAM. It is never moved to disk.')),
                ('swap_total', models.PositiveBigIntegerField(help_text='total swap memory in bytes')),
                ('swap_used', models.PositiveBigIntegerField(help_text='used swap memory in bytes')),
                ('swap_free', models.PositiveBigIntegerField(help_text='free swap memory in bytes')),
                ('swap_percent', models.FloatField(help_text='the percentage usage calculated as (total - available) / total * 100')),
                ('swap_sin', models.PositiveBigIntegerField(help_text='the number of bytes the system has swapped in from disk (cumulative)')),
                ('swap_sout', models.PositiveBigIntegerField(help_text='the number of bytes the system has swapped out from disk (cumulative)')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest_server.report')),
            ],
        ),
    ]
