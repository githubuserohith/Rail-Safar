# Generated by Django 4.0.8 on 2022-11-04 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('railways', '0015_fare'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trains',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='railways.fare'),
        ),
    ]