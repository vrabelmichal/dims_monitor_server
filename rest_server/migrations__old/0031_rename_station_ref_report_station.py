# Generated by Django 3.2.7 on 2022-01-04 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_server', '0030_remove_report_station'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='station_ref',
            new_name='station',
        ),
    ]