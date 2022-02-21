# Generated by Django 4.0.2 on 2022-02-03 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_server', '0040_remove_environmentlogupload_unique_pair_station_captured_hour'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='environmentlogmeasurement',
            name='unique_pair_datetime_station',
        ),
        migrations.AddConstraint(
            model_name='environmentlogmeasurement',
            constraint=models.UniqueConstraint(fields=('measurement_datetime', 'log_upload'), name='unique_pair_datetime_log_upload'),
        ),
        migrations.AddConstraint(
            model_name='environmentlogmeasurement',
            constraint=models.UniqueConstraint(fields=('measurement_datetime', 'station'), name='unique_pair_datetime_station'),
        ),
    ]