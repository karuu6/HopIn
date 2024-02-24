from django.db import models

# Create your models here.
class Ride(models.Model):
    text = models.CharField(max_length=200)

class Trips(models.Model):
    trip_id = models.AutoField(primary_key=True)
    driver_id = models.IntegerField()
    hopper_id = models.JSONField(default=list) 
    ride_status = models.CharField(
        max_length=20,
        choices=[
            ('posted', 'Posted'),
            ('in-progress', 'In Progress'),
            ('done', 'Done')
        ],
        default='posted'
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    pickup_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    pickup_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    dropoff_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    dropoff_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    open_seats = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Trip {self.trip_id} by Driver {self.driver_id}" 

class HopperRequests(models.Model):
    trip_id = models.ForeignKey('Trips', on_delete=models.CASCADE)
    hopper_id = models.IntegerField()
    hopper_status = models.CharField(
        max_length=20,
        choices=[
            ('requested', 'Requested'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected')
        ],
        default='requested'
    )

    def __str__(self):
        return f"Hopper {self.hopper_id} for Trip {self.trip_id} - {self.get_hopper_status_display()}"
