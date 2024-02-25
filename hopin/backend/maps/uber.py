import requests

def get_uber_price_estimates(start_latitude, start_longitude, end_latitude, end_longitude):
    url = "https://api.uber.com/v1.2/estimates/price"
    
    parameters = {
        'start_latitude': start_latitude,
        'start_longitude': start_longitude,
        'end_latitude': end_latitude,
        'end_longitude': end_longitude,
    }
    
    headers = {
        'Authorization': 'Token {YOUR_SERVER_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(url, params=parameters, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}"

# Example usage
start_latitude = 37.7752315
start_longitude = -122.418075
end_latitude = 37.621313
end_longitude = -122.378955

print(get_uber_price_estimates(start_latitude, start_longitude, end_latitude, end_longitude))
