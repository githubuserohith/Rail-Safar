# Generated by Django 4.0.8 on 2022-11-01 18:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('railways', '0009_alter_psg_doj'),
    ]

    operations = [
        migrations.AlterField(
            model_name='psg',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
