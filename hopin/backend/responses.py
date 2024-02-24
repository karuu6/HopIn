from .models import Trip
from .maps import google_maps 

class TripResponse:
    def __init__(self, trip: Trip):
        self.trip = trip

    def to_dict(self):
        pickup_address = google_maps.convert_coords((self.trip.pickup_latitude, self.trip.pickup_longitude))
        dropoff_address = google_maps.convert_coords((self.trip.dropoff_latitude, self.trip.dropoff_longitude))

        return {
            "trip_id": self.trip.id,
            "driver_username": self.trip.driver_id.username,
            "driver_rating": self.trip.driver_id.profile.driver_rating,
            "date": self.trip.date,
            "start_time": self.trip.start_time.strftime('%H:%M:%S'),
            "end_time": self.trip.end_time.strftime('%H:%M:%S'),
            "open_seats": self.trip.open_seats,
            "price": str(self.trip.price),
            "ride_status": self.trip.ride_status,
            'pickup_address' : pickup_address,
            'dropoff_address' : dropoff_address
        }