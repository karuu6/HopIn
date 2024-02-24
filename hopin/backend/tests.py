from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Trip, Profile
from django.utils import timezone
from datetime import timedelta
from unittest.mock import patch
from decimal import Decimal
from .maps.google_maps import find_within_radius
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

class TripSearchTestCase(TestCase):

    """
    Champaign, IL (40.1164204, -88.2433829)
    Chicago, IL (41.8781136, -87.6297982)
    Savoy, IL (40.054753, -88.2517165)
    Evanston, IL (42.0450722, -87.68769689999999)

    trips db should have trip from savoy to evanston and other boofoo trips
    request is from champaign to chicago, with radius of x that should include this trip only
    other trips have same exact timings
    this tests that the filtering works fine
    """

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='hopper', password='testpassword')
        self.client = APIClient()
        self.client.login(username='hopper', password='testpassword')
        Profile.objects.create(user=self.user, picture='default.png', driver_rating=-1, hopper_rating=-1)
        # Create a trip
        self.trip = Trip.objects.create(
            driver_id=self.user,
            date='2024-02-24',
            start_time='10:00',
            end_time='11:00',
            pickup_latitude=Decimal('40.712776'),
            pickup_longitude=Decimal('-74.005974'),
            dropoff_latitude=Decimal('40.712776'),
            dropoff_longitude=Decimal('-73.005974'),
            open_seats=3,
            price=Decimal('50.00')
        )

        #correct trip
        self.correct_trip = Trip.objects.create(
            driver_id=self.user,
            date='2024-02-24',
            start_time='10:00',
            end_time='11:00',
            pickup_latitude=Decimal('40.054753'),
            pickup_longitude=Decimal('-88.2517165'),
            dropoff_latitude=Decimal('42.0450722'),
            dropoff_longitude=Decimal('-87.687696899'),
            open_seats=3,
            price=Decimal('50.00')
        )

        response = self.client.post(reverse('token_obtain_pair'), {'username': 'hopper', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    
    @patch('backend.views.google_maps.convert_address')
    @patch('backend.views.google_maps.convert_coords')
    def test_search_view_filter(self, mock_convert_coords, mock_convert_address):
        # Mock the google_maps method responses
        def mocked_convert_coords(lat, long):
            if (lat, long) == (40.1164204, -88.2433829):
                return 'Champaign, IL'
            if (lat, long) == (41.8781136, -87.6297982):
                return 'Chicago, IL'
        mock_convert_coords.side_effect = mocked_convert_coords

        def mocked_convert_address(address):
            if address == 'Champaign, IL':
                return 40.1164204, -88.2433829
            if address == 'Chicago, IL':
                return 41.8781136, -87.6297982
        mock_convert_address.side_effect = mocked_convert_address

        c = self.client
        response = c.get(reverse('search'), {
            'date': '2024-02-24',
            'radius': '50',
            'pickup_loc': 'Champaign, IL',
            'dropoff_loc': 'Chicago, IL',
            'arrive_by': '11:00',
            'leave_by': '10:00'
        })

        self.assertEqual(len(response.json()['trips']), 1)
        self.assertEqual(response.json()['trips'][0]['trip_id'], self.correct_trip.id)
    
    

    @patch('backend.views.google_maps.convert_address')
    @patch('backend.views.google_maps.find_within_radius')
    @patch('backend.views.google_maps.convert_coords')
    def test_search_view(self, mock_convert_coords, mock_find_within_radius, mock_convert_address):
        # Mock the google_maps method responses
        mock_convert_address.return_value = (40.7128, -74.0060)
        mock_find_within_radius.return_value = {self.trip.id: (self.trip.pickup_latitude, self.trip.pickup_longitude)}
        mock_convert_coords.return_value = "123 Main Street"

        c = self.client
        response = c.get(reverse('search'), {
            'date': '2024-02-24',
            'radius': '10',
            'pickup_loc': '123 Main Street',
            'dropoff_loc': '456 Elm Street',
            'arrive_by': '11:00',
            'leave_by': '10:00'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['trips'][0]['trip_id'], self.trip.id)

    def test_search_view_missing_parameters(self):
        c = self.client
        response = c.get(reverse('search'), {
            'date': '2024-02-24',
            # 'radius' parameter is missing
            'pickup_loc': '123 Main Street',
            'dropoff_loc': '456 Elm Street',
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Missing or invalid parameters')


class PastDrivesTests(TestCase):
    s_time = timezone.now()
    s_time2 = timezone.now() + timedelta(hours=6)
    s_time3 = timezone.now() + timedelta(hours=12)

    def setUp(self):
        # Create a test user and log them in
        self.user = User.objects.create_user(username='driver', password='testpassword')
        self.client = APIClient()
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
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'driver', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

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
        self.client = APIClient()
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
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'hopper', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

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


class UtilsTestCase(TestCase):

    def test_find_within_radius(self):
        # Define a set of coordinates and a query point
        coordinates = [
            ((40.7128, -74.0060), 1),  # New York City
            ((34.0522, -118.2437), 2),  # Los Angeles
            ((41.8781, -87.6298), 3),   # Chicago
        ]
        query_point = (39.9526, -75.1652)  # Philadelphia
        radius = 100  # miles

        # Call the function
        results = find_within_radius(coordinates, query_point, radius)

        # Assertions
        self.assertIn(1, results)  # NYC should be within the radius
        self.assertNotIn(3, results)  # Chicago should not
        self.assertNotIn(2, results)  # Los Angeles should not

    def test_find_within_radius_no_results(self):
        # Define a set of coordinates and a query point
        coordinates = [
            ((40.7128, -74.0060), 1),  # New York City
            ((34.0522, -118.2437), 2),  # Los Angeles
        ]
        query_point = (48.8566, 2.3522)  # Paris, France
        radius = 1000  # miles

        # Call the function
        results = find_within_radius(coordinates, query_point, radius)

        # Assertions
        self.assertEqual(results, {})  # No results should be within the radius