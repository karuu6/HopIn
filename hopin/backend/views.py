from django.shortcuts import get_object_or_404
from .models import Trip, HopperRequest
from .responses import TripResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

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