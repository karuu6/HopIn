from django.shortcuts import render
from django.http import HttpResponse
from .models import Ride

# Create your views here.
def index(request):
    s = ""
    ride_list = Ride.objects.all()
    for ride in ride_list:
        s += f"<a href={ride.id}> {ride.id}</a>"
    return HttpResponse(s)

def view_ride(request, ride_id):
    r = Ride.objects.get(pk=ride_id)
    return HttpResponse(r.text)