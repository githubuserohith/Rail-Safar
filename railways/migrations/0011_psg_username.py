# Generated by Django 4.0.8 on 2022-11-02 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('railways', '0010_alter_psg_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='psg',
            name='username',
            field=models.CharField(default='default', max_length=50),
            preserve_default=False,
        ),
    ]
