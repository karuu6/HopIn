from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils.dateparse import parse_date, parse_time
from .models import *
from .maps import google_maps
from .serializers import SignUpSerializer, TripSerializer, HopperRequestSerializer

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.contrib.auth.models import User
from django.db.models import F
from rest_framework import status


class Search(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
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
        print('pre process:', trips)

        pickup_trip_coordinates = [((trip.pickup_latitude, trip.pickup_longitude), trip.id) for trip in trips]
        filtered_for_pickup_trip_ids = google_maps.find_within_radius(pickup_trip_coordinates, (pickup_latitude, pickup_longitude), radius)

        dropoff_trip_coordinates = [((trip.dropoff_latitude, trip.dropoff_longitude), trip.id) for trip in trips if trip.id in filtered_for_pickup_trip_ids]
        filtered_for_dropoff_trip_ids = google_maps.find_within_radius(dropoff_trip_coordinates, (dropoff_latitude, dropoff_longitude), radius)
        
        # Convert the Trip objects into a list of dictionaries (or any other format you need) to return as JSON
        trips_data = []

        for trip in trips:
            if trip.id in filtered_for_dropoff_trip_ids:
                trips_data.append(TripSerializer(trip).data)
        
        print('post process: ',trips_data)
        return Response({'trips': trips_data})


class PastDrives(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        user = request.user
        # Using the 'driven_trips' related_name to filter trips where the user is a driver
        past_trips = user.driven_trips.filter(ride_status=2)

        trips_data = [TripSerializer(trip).data for trip in past_trips]
        
        return Response({"driver_trips": trips_data})


class PastHops(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        
        # Using the 'hopped_trips' related_name to filter trips where the user is a hopper
        past_hops = user.hopped_trips.filter(ride_status=2)
        
        hops_data = [TripSerializer(hop).data for hop in past_hops]
        
        return Response({"past_hops": hops_data})

class CurrentTripsForDriver(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        # Using the 'driven_trips' related_name to filter trips where the user is a driver
        past_trips = user.driven_trips.exclude(ride_status=2)

        trips_data = [TripSerializer(trip).data for trip in past_trips]
        
        return Response({"past_trips": trips_data})

class CurrentHopperRequests(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, trip_id):
        trip = get_object_or_404(Trip, pk=trip_id)
        
        hopper_requests = trip.trips_hopper_requests.all()

        requests_data = [HopperRequestSerializer(request).data for request in hopper_requests]
        
        return Response({"hopper_requests": requests_data})


class HoppersRequestsStatus(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_id = request.user.id
        
        hopper_requests = HopperRequest.objects.filter(hopper_id=user_id)
        
        requests_data = [HopperRequestSerializer(request).data for request in hopper_requests]
        
        return JsonResponse({"hopper_requests": requests_data})


class SignUp(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer


class PostTrip(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TripSerializer

class AcceptHopperRequest(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, trip_id):
        # Get the trip object
        trip = get_object_or_404(Trip, pk=trip_id)
        
        # Check if there are open seats
        if trip.open_seats <= 0:
            return Response({"error": "No open seats available"}, status=status.HTTP_400_BAD_REQUEST)

        # Since you're accepting the hopper request, you might not need to deserialize request data here
        # Directly add the current user to hoppers and decrement open_seats
        trip.open_seats -= 1
        trip.hoppers.add(request.user)  # Add the current user to hoppers
        trip.save()

        # No need to use serializer for adding hopper in this case
        return Response(None, status=status.HTTP_201_CREATED)

class DeclineHopperRequest(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, hopper_request_id):
        # Get the HopperRequest object
        hopper_request = get_object_or_404(HopperRequest, pk=hopper_request_id)

        # Check if the current user is the driver of the trip to authorize decline action
        if hopper_request.trip_id.driver_id != request.user:
            return Response({"error": "You are not authorized to decline this hopper request"}, status=status.HTTP_403_FORBIDDEN)

        # Change the hopper request status to 2 (declined)
        hopper_request.hopper_status = 2
        hopper_request.save()

        # Return a success response
        return Response({"message": "Hopper request declined successfully"}, status=status.HTTP_200_OK)


class PostHopperRequest(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = HopperRequestSerializer
