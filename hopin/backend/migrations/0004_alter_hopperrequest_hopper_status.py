# Generated by Django 5.0.2 on 2024-02-25 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_trip_dropoff_location_trip_pickup_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hopperrequest',
            name='hopper_status',
            field=models.IntegerField(default=0),
        ),
    ]