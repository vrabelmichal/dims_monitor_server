# Generated by Django 3.2.7 on 2021-12-26 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_server', '0018_auto_20211021_2139'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='retrieved_utc',
            field=models.DateTimeField(default='1970-01-01T0:0:0'),
            preserve_default=False,
        ),
    ]
