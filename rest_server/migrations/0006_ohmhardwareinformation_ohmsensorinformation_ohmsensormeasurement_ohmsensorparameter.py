# Generated by Django 3.2.7 on 2021-10-19 18:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rest_server', '0005_auto_20210908_1753'),
    ]

    operations = [
        migrations.CreateModel(
            name='OhmHardwareInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='OhmSensorInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('hardware', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest_server.ohmhardwareinformation')),
            ],
        ),
        migrations.CreateModel(
            name='OhmSensorParameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('value', models.FloatField()),
                ('default_value', models.FloatField()),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest_server.ohmsensorinformation')),
            ],
        ),
        migrations.CreateModel(
            name='OhmSensorMeasurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(help_text='Datetime of the measurement')),
                ('value', models.FloatField()),
                ('value_max', models.FloatField()),
                ('value_min', models.FloatField()),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest_server.report')),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest_server.ohmsensorinformation')),
            ],
        ),
    ]
