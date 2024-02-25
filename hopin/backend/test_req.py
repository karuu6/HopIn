import requests

headers = {
    'Content-Type': 'application/json;',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA4ODIxNzU1LCJpYXQiOjE3MDg4MjE0NTUsImp0aSI6Ijc0MWIxOWQxMTE3YzQ4MWViZjc0MzRlNTVkOWM2YzEyIiwidXNlcl9pZCI6M30.r_r2G834jNvIsIbx0OOR3D3PbhIIkCWBsMIdsTd9S8A'
}

data = {
    'date': '2025-01-01',
    'start_time': '23:01:01',
    'pickup_location': 'Champaign, IL',
    'dropoff_location': 'Chicago, IL',
    'open_seats': 1,
    'price': 23.1
}

r = requests.post('http://127.0.0.1:8000/api/post_trip/', json=data, headers=headers)
print(r.status_code)

print(r.json())