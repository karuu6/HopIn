from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Ride(models.Model):
    text = models.CharField(max_length=200)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Delete profile when user is deleted
    picture = models.ImageField(default='default.png', upload_to='profile_pics')
    driver_rating = models.IntegerField(default=-1)
    hopper_rating = models.IntegerField(default=-1)
