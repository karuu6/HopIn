from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils.dateparse import parse_date, parse_time
from .models import *
from .maps import google_maps
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Trip, HopperRequest
from .responses import TripResponse


# Create your views here.
def index(request):
    return HttpResponse("Hello World")

# def view_ride(request, ride_id):
#     r = Ride.objects.get(pk=ride_id)
#     return HttpResponse(r.text)
#225 S Canal St, Chicago, IL 60606

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('date', openapi.IN_QUERY, description="Date of the trip", type=openapi.TYPE_STRING),
        openapi.Parameter('radius', openapi.IN_QUERY, description="Search radius in miles", type=openapi.TYPE_NUMBER),
        openapi.Parameter('pickup_loc', openapi.IN_QUERY, description="Pickup location address", type=openapi.TYPE_STRING),
        openapi.Parameter('dropoff_loc', openapi.IN_QUERY, description="Dropoff location address", type=openapi.TYPE_STRING),
        openapi.Parameter('arrive_by', openapi.IN_QUERY, description="Time to arrive by", type=openapi.TYPE_STRING),
        openapi.Parameter('leave_by', openapi.IN_QUERY, description="Time to leave by", type=openapi.TYPE_STRING),
    ],
    responses={200: 'Success'}
)
@api_view(['GET'])
def search(request):
    date_str = request.GET.get('date', None)
    radius_str = request.GET.get('radius', None)
    pickup_loc_str = request.GET.get('pickup_loc', None)
    dropoff_loc_str = request.GET.get('dropoff_loc', None)

    arrive_by_str = request.GET.get('arrive_by', None)
    leave_by_str = request.GET.get('leave_by', None)

    if not date or not radius_str or not pickup_loc_str or not dropoff_loc_str:
            return JsonResponse({'error': 'Missing or invalid arrive_by parameters'}, status=400)
    
    # Parse the date and time strings into datetime.date and datetime.time objects
    date = parse_date(date_str) if date_str else None
    radius = float(radius_str)

    pickup_latitude, pickup_longitude = google_maps.convert_address(pickup_loc_str)
    dropoff_latitude, dropoff_longitude = google_maps.convert_address(dropoff_loc_str)


    arrive_by = parse_time(arrive_by_str) if arrive_by_str else None
    leave_by = parse_time(leave_by_str) if leave_by_str else None
    
    filter_kwargs = {}
    
    # Add conditions to the dictionary based on the presence of parameters
    filter_kwargs['date'] = date

    if arrive_by:
        filter_kwargs['end_time__lte'] = arrive_by
    if leave_by:
        filter_kwargs['start_time__lte'] = leave_by
    

    trips = Trip.objects.filter(**filter_kwargs).order_by('price')

    pickup_trip_coordinates = [((trip.pickup_latitude, trip.pickup_longitude), trip.id) for trip in trips]
    filtered_for_pickup_trip_ids = google_maps.find_within_radius(pickup_trip_coordinates, (pickup_latitude, pickup_longitude), radius)

    dropoff_trip_coordinates = [((trip.dropoff_latitude, trip.dropoff_longitude), trip.id) for trip in trips if trip.id in filtered_for_pickup_trip_ids]
    filtered_for_dropoff_trip_ids = google_maps.find_within_radius(dropoff_trip_coordinates, (dropoff_latitude, dropoff_latitude), radius)
    

    
    # Convert the Trip objects into a list of dictionaries (or any other format you need) to return as JSON
    trips_data = []

    for trip in trips:
        if trip.id in filtered_for_dropoff_trip_ids:
            pickup_address = google_maps.convert_coords((trip.pickup_latitude, trip.pickup_longitude))
            dropoff_address = google_maps.convert_coords((trip.dropoff_latitude, trip.dropoff_longitude))
            trips_data.append({'trip_id': trip.id,
                                'driver_id': trip.driver_id.id,
                                'date': trip.date,
                                'start_time': trip.start_time,
                                'end_time': trip.end_time,
                                'price': trip.price,
                                'pickup_address' : pickup_address,
                                'dropoff_address' : dropoff_address})
    
    return JsonResponse({'trips': trips_data})
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
