from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Trip, HopperRequest
from .responses import TripResponse


# Create your views here.
def index(request):
    return HttpResponse("Hello World")

@login_required
def past_drives(request):
    user = request.user
    
    # Using the 'driven_trips' related_name to filter trips where the user is a driver
    past_trips = user.driven_trips.filter(ride_status=2)

    trips_data = [TripResponse(trip).to_dict() for trip in past_trips]
    
    return JsonResponse({"past_trips": trips_data})

@login_required
def past_hops(request):
    user = request.user
    
    # Using the 'hopped_trips' related_name to filter trips where the user is a hopper
    past_hops = user.hopped_trips.filter(ride_status=2)
    
    hops_data = [TripResponse(hop).to_dict() for hop in past_hops]
    
    return JsonResponse({"past_hops": hops_data})
