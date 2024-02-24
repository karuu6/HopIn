from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils.dateparse import parse_date, parse_time
from .models import *
from .maps import google_maps
from .responses import TripResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


def search(request):
    date_str = request.GET.get('date', None)
    radius_str = request.GET.get('radius', None)
    pickup_loc_str = request.GET.get('pickup_loc', None)
    dropoff_loc_str = request.GET.get('dropoff_loc', None)

    arrive_by_str = request.GET.get('arrive_by', None)
    leave_by_str = request.GET.get('leave_by', None)

    if not date_str or not radius_str or not pickup_loc_str or not dropoff_loc_str:
            return JsonResponse({'error': 'Missing or invalid parameters'}, status=400)
    
    # Parse the date and time strings into datetime.date and datetime.time objects
    date = parse_date(date_str) if date_str else None
    radius = float(radius_str)

    pickup_latitude, pickup_longitude = google_maps.convert_address(pickup_loc_str)
    dropoff_latitude, dropoff_longitude = google_maps.convert_address(dropoff_loc_str)


    arrive_by = parse_time(arrive_by_str) if arrive_by_str else None
    leave_by = parse_time(leave_by_str) if leave_by_str else None
    
    filter_kwargs = {'open_seats__gt' : 0}
    
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
    filtered_for_dropoff_trip_ids = google_maps.find_within_radius(dropoff_trip_coordinates, (dropoff_latitude, dropoff_longitude), radius)
    

    
    # Convert the Trip objects into a list of dictionaries (or any other format you need) to return as JSON
    trips_data = []

    for trip in trips:
        if trip.id in filtered_for_dropoff_trip_ids:
            trips_data.append(TripResponse(trip).to_dict())
    
    return JsonResponse({'trips': trips_data})

class PastDrives(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        user = request.user
        # Using the 'driven_trips' related_name to filter trips where the user is a driver
        past_trips = user.driven_trips.filter(ride_status=2)

        trips_data = [TripResponse(trip).to_dict() for trip in past_trips]
        
        return Response({"past_trips": trips_data})

class PastHops(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        
        # Using the 'hopped_trips' related_name to filter trips where the user is a hopper
        past_hops = user.hopped_trips.filter(ride_status=2)
        
        hops_data = [TripResponse(hop).to_dict() for hop in past_hops]
        
        return Response({"past_hops": hops_data})