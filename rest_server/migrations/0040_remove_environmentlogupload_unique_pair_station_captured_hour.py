# Generated by Django 4.0.2 on 2022-02-03 22:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_server', '0039_rename_is_finished_environmentlogupload_is_historical'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='environmentlogupload',
            name='unique_pair_station_captured_hour',
        ),
    ]
