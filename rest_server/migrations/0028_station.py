# Generated by Django 3.2.7 on 2022-01-04 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_server', '0027_auto_20220104_1312'),
    ]

    operations = [
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
    ]