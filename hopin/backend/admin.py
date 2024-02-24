from django.contrib import admin
from .models import Ride, Trip, HopperRequest

# Register your models here.

admin.site.register((Ride, Trip, HopperRequest))
