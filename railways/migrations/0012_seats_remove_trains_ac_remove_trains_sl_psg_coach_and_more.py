# Generated by Django 4.0.8 on 2022-11-02 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('railways', '0011_psg_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('train', models.IntegerField()),
                ('date', models.CharField(max_length=10)),
                ('from_st', models.CharField(max_length=10)),
                ('to_st', models.CharField(max_length=10)),
                ('ac', models.PositiveSmallIntegerField(default=3)),
                ('sl', models.PositiveSmallIntegerField(default=5)),
            ],
        ),
        migrations.RemoveField(
            model_name='trains',
            name='ac',
        ),
        migrations.RemoveField(
            model_name='trains',
            name='sl',
        ),
        migrations.AddField(
            model_name='psg',
            name='coach',
            field=models.CharField(default=0, max_length=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='psg',
            name='destination',
            field=models.CharField(default='0', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='psg',
            name='origin',
            field=models.CharField(default='0', max_length=10),
            preserve_default=False,
        ),
    ]
