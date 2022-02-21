# Generated by Django 3.2.7 on 2022-01-04 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_server', '0022_auto_20220104_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ufocaptureoutputentry',
            name='cam',
            field=models.CharField(blank=True, help_text='Value of attribute "cam" of ufocapture_record inside UFOCapture XML file.', max_length=32, null=True),
        ),
    ]