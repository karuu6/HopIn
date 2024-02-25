from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Delete profile when user is deleted
    picture = models.ImageField(default='default.png', upload_to='profile_pics')
    driver_rating = models.IntegerField(default=-1)
    hopper_rating = models.IntegerField(default=-1)

class Trip(models.Model):
    driver_id = models.ForeignKey(User, related_name='driven_trips', on_delete=models.CASCADE)
    hoppers = models.ManyToManyField(User, related_name='hopped_trips', blank=True) 
    ride_status = models.IntegerField(default=0) # 0: posted, 1: in-progress, 2: done
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    pickup_location = models.CharField(max_length = 256, default = '')
    dropoff_location = models.CharField(max_length = 256, default = '')
    pickup_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    pickup_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    dropoff_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    dropoff_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    open_seats = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Trip {self.id} by Driver {self.driver_id}" 

class HopperRequest(models.Model):
    trip_id = models.ForeignKey(Trip, related_name='trips_hopper_requests', on_delete=models.CASCADE)
    hopper_id = models.ForeignKey(User, related_name='hoppers_hopper_requests', on_delete=models.CASCADE)
    hopper_status = models.DateField(default=0) # 0: requested, 1: accepted, 2: rejected

    def __str__(self):
        return f"Hopper {self.hopper_id} for Trip {self.trip_id} - {self.get_hopper_status_display()}"

