# Generated by Django 3.2.7 on 2022-01-04 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rest_server', '0031_rename_station_ref_report_station'),
    ]

    operations = [
        migrations.AddField(
            model_name='ufocaptureoutputentry',
            name='station',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rest_server.station'),
        ),
        migrations.AlterField(
            model_name='report',
            name='station',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='rest_server.station'),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='ufocaptureoutputentry',
            constraint=models.UniqueConstraint(fields=('station', 'clip_filename'), name='unique_pair_station_clip'),
        ),
    ]