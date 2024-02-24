from django.db import models

# Create your models here.
class Ride(models.Model):
    text = models.CharField(max_length=200)
