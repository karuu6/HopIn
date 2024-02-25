from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth.models import User
from .models import Trip, Profile, HopperRequest
from .maps import google_maps


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'username': {'required': False},
            'password': {'required': False, 'write_only': True},
        }

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()

        profile = Profile(user = user)
        profile.save()

        return user

class TripSerializer(serializers.ModelSerializer):
    driver_username = serializers.SerializerMethodField('get_driver_username')

    def get_driver_username(self, obj):
        return obj.driver_id.username

    class Meta:
        model = Trip
        fields = '__all__'
        extra_kwargs = {
            'driver_id': {'required': False},
            'hoppers': {'required': False},
            'ride_status': {'required': False},
            'pickup_latitude': {'required': False},
            'pickup_longitude': {'required': False},
            'dropoff_latitude': {'required': False},
            'dropoff_longitude': {'required': False},
            'end_time': {'required': False},
        }

    def validate(self, data):
        pc = google_maps.convert_address(data['pickup_location'])
        if pc is None:
            raise serializers.ValidationError("invalid pickup location")
        dc = google_maps.convert_address(data['dropoff_location'])
        if dc is None:
            raise serializers.ValidationError("invalid dropoff location")
        data['pickup_latitude'] = pc[0]
        data['pickup_longitude'] = pc[1]
        data['dropoff_latitude'] = dc[0]
        data['dropoff_longitude'] = dc[1]
        return data
    
    def create(self, validated_data):
        trip = Trip.objects.create(
            driver_id = self.context['request'].user,
            date = validated_data['date'],
            start_time = validated_data['start_time'],
            end_time = validated_data['start_time'],
            pickup_location = validated_data['pickup_location'],
            dropoff_location = validated_data['dropoff_location'],
            pickup_latitude = validated_data['pickup_latitude'],
            pickup_longitude = validated_data['pickup_longitude'],
            dropoff_latitude = validated_data['dropoff_latitude'],
            dropoff_longitude = validated_data['dropoff_longitude'],
            open_seats = validated_data['open_seats'],
            price = validated_data['price'],
        )
        trip.save()
        return trip
    
class HopperRequestSerializer(serializers.ModelSerializer):
    hopper_username = serializers.SerializerMethodField('get_hopper_username')
    hopper_rating = serializers.SerializerMethodField('get_hopper_rating')

    def get_hopper_username(self, obj):
        return obj.hopper_id.username

    def get_hopper_rating(self, obj):
        return obj.hopper_id.profile.hopper_rating

    class Meta:
        model = HopperRequest
        fields = '__all__'

        extra_kwargs = {
            'hopper_id': {'required': False},
            'hopper_status': {'required': False},
        }
    
    def create(self, validated_data):
        hopper_request = HopperRequest(
            trip_id = validated_data['trip_id'],
            hopper_id = self.context['request'].user,
            hopper_status = 0,
        )

        hopper_request.save()
        return hopper_request


