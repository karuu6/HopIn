import googlemaps
import os
from math import radians, cos, sin, sqrt, atan2

API_KEY = os.environ.get('GOOGLE_API_KEY')

gmaps = googlemaps.Client(key=API_KEY)

def find_within_radius(coordinates, query_point, radius):
    """
    :param coordinates: List of tuples, where each tuple is ((latitude, longitude), trip_id)
    :param query_point: Tuple of (latitude, longitude) for the query point
    :param radius: Radius in miles
    :return: dictionary of {trip_id : (latitude, longitude)} if latitude and longitude fit in raidus of query point
    """
    def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in miles
        R = 3958.8
        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        # Difference in coordinates
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        # Haversine formula
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c
        return distance
    
    lat_query, lon_query = query_point
    return {coord[1] : coord[0] for coord in coordinates if haversine(lat_query, lon_query, coord[0][0], coord[0][1]) <= radius}



#address -> string: valid address
#returns -> tuple(float, float): latitude, longitude
def convert_address(address):
    geocode_result = gmaps.geocode(address)
    if geocode_result:
        latitude = geocode_result[0]['geometry']['location']['lat']
        longitude = geocode_result[0]['geometry']['location']['lng']
        #print(f"Coordinates for '{address}': Latitude {latitude}, Longitude {longitude}")
        return latitude, longitude
    else:
        print("Address not found.")

def convert_coords(latitude, longitude):
    reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude))

    if reverse_geocode_result:
        address = reverse_geocode_result[0]['formatted_address']
        #print(f"Address for ({latitude}, {longitude}): {address}")
        return address
    else:
        print("Address not found.")
