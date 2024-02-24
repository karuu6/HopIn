from django.contrib import admin
from .models import Profile, Trip, HopperRequest

# Register your models here.
admin.site.register((Profile, Trip, HopperRequest))
