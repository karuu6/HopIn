from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Trip, Profile
from django.utils import timezone
from datetime import timedelta
from unittest.mock import patch



class PastDrivesTests(TestCase):
    s_time = timezone.now()
    s_time2 = timezone.now() + timedelta(hours=6)
    s_time3 = timezone.now() + timedelta(hours=12)

    def setUp(self):
        # Create a test user and log them in
        self.user = User.objects.create_user(username='driver', password='testpassword')
        self.client = Client()
        self.client.login(username='driver', password='testpassword')
        Profile.objects.create(user=self.user, picture='default.png', driver_rating=-1, hopper_rating=-1)

        # Create test trips
        Trip.objects.create(driver_id=self.user, date=timezone.now(), start_time=self.s_time, 
                            end_time=self.s_time + timedelta(hours=2), pickup_latitude='40.1100516', 
                            pickup_longitude='-88.2341611', dropoff_latitude='1.000000', 
                            dropoff_longitude='1.000000', open_seats=4, price='10.00', ride_status=2)
        
        Trip.objects.create(driver_id=self.user, date=timezone.now(), start_time=self.s_time2, 
                            end_time=self.s_time2 + timedelta(hours=2), pickup_latitude='1.000000', 
                            pickup_longitude='1.000000', dropoff_latitude='40.1100516', 
                            dropoff_longitude='-88.2341611', open_seats=2, price='20.00', ride_status=2)
        
        Trip.objects.create(driver_id=self.user, date=timezone.now(), start_time=self.s_time3, 
                            end_time=self.s_time2 + timedelta(hours=2), pickup_latitude='10.000000', 
                            pickup_longitude='10.000000', dropoff_latitude='10.000000', 
                            dropoff_longitude='10.000000', open_seats=3, price='100.00', ride_status=0)
    

    @patch('backend.maps.google_maps.convert_coords')
    def test_past_drives(self, mock_convert_coords):
        mock_convert_coords.side_effect = ['Mocked Pickup Address', 'Mocked Drop-off Address', 'Mocked Pickup Address 2', 'Mocked Drop-off Address 2']

        response = self.client.get(reverse('past_drives'))
        formatted_start_time = self.s_time.strftime('%H:%M:%S')
        formatted_end_time = (self.s_time + timedelta(hours=2)).strftime('%H:%M:%S')

        formatted_start_time2 = self.s_time2.strftime('%H:%M:%S')
        formatted_end_time2 = (self.s_time2 + timedelta(hours=2)).strftime('%H:%M:%S')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"past_trips": [
                {
                    "trip_id": 1,
                    "driver_username": 'driver',
                    "driver_rating": -1,
                    "date": str(timezone.now().date()),
                    "start_time": formatted_start_time,
                    "end_time": formatted_end_time,
                    "open_seats": 4,
                    "price": "10.00",
                    'pickup_address' : "Mocked Pickup Address",
                    'dropoff_address' : "Mocked Drop-off Address"
                }, 
                {
                    "trip_id": 2,
                    "driver_username": 'driver',
                    "driver_rating": -1,
                    "date": str(timezone.now().date()),
                    "start_time": formatted_start_time2,
                    "end_time": formatted_end_time2,
                    "open_seats": 2,
                    "price": "20.00",
                    'pickup_address' : "Mocked Pickup Address 2",
                    'dropoff_address' : "Mocked Drop-off Address 2"
                }
            ]}
        )


class PastHopsTests(TestCase):
    s_time = timezone.now()
    s_time2 = timezone.now() + timedelta(hours=6)

    def setUp(self):
        self.maxDiff = None
        # Create a test user and log them in
        self.user = User.objects.create_user(username='hopper', password='testpassword')
        self.client = Client()
        self.client.login(username='hopper', password='testpassword')
        Profile.objects.create(user=self.user, picture='default.png', driver_rating=-1, hopper_rating=-1)

        # Create another user for driving
        self.driver = User.objects.create_user(username='driver', password='testpassword')
        Profile.objects.create(user=self.driver, picture='default.png', driver_rating=-1, hopper_rating=-1)

        # Create test trips
        trip1 = Trip.objects.create(driver_id=self.driver, date=timezone.now(), start_time=self.s_time, 
                                    end_time=self.s_time + timedelta(hours=2), pickup_latitude='40.1100516', 
                                    pickup_longitude='-88.2341611', dropoff_latitude='1.000000', 
                                    dropoff_longitude='1.000000', open_seats=4, price='10.00', ride_status=2)
        
        trip2 = Trip.objects.create(driver_id=self.driver, date=timezone.now(), start_time=self.s_time2, 
                                    end_time=self.s_time2 + timedelta(hours=2), pickup_latitude='1.000000', 
                                    pickup_longitude='1.000000', dropoff_latitude='40.1100516', 
                                    dropoff_longitude='-88.2341611', open_seats=2, price='20.00', ride_status=2)

        # Add the test user as a hopper to the trips
        trip1.hoppers.add(self.user)
        trip2.hoppers.add(self.user)

    @patch('backend.maps.google_maps.convert_coords')
    def test_past_hops(self, mock_convert_coords):
        mock_convert_coords.side_effect = ['Mocked Pickup Address for Hops', 'Mocked Drop-off Address for Hops', 'Mocked Pickup Address 2 for Hops', 'Mocked Drop-off Address 2 for Hops']

        response = self.client.get(reverse('past_hops'))

        formatted_start_time = self.s_time.strftime('%H:%M:%S')
        formatted_end_time = (self.s_time + timedelta(hours=2)).strftime('%H:%M:%S')

        formatted_start_time2 = self.s_time2.strftime('%H:%M:%S')
        formatted_end_time2 = (self.s_time2 + timedelta(hours=2)).strftime('%H:%M:%S')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"past_hops": [
                {
                    "trip_id": 1,
                    "driver_username": 'driver',
                    "driver_rating": -1,
                    "date": str(timezone.now().date()),
                    "start_time": formatted_start_time,
                    "end_time": formatted_end_time,
                    "open_seats": 4,
                    "price": "10.00",
                    'pickup_address' : "Mocked Pickup Address for Hops",
                    'dropoff_address' : "Mocked Drop-off Address for Hops"
                }, 
                {
                    "trip_id": 2,
                    "driver_username": 'driver',
                    "driver_rating": -1,
                    "date": str(timezone.now().date()),
                    "start_time": formatted_start_time2,
                    "end_time": formatted_end_time2,
                    "open_seats": 2,
                    "price": "20.00",
                    'pickup_address' : "Mocked Pickup Address 2 for Hops",
                    'dropoff_address' : "Mocked Drop-off Address 2 for Hops"
                }
            ]}
        )
