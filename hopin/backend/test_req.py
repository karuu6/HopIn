import requests

headers = {
    'Content-Type': 'application/json;',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA4ODIzMjQzLCJpYXQiOjE3MDg4MjI5NDMsImp0aSI6IjIxZTNlZWNjZDYwZTQ1MTc4OWI4ZTZmYzExZmQ3NjYzIiwidXNlcl9pZCI6M30.Ifjc-OvLxIz8_F65dJSeQToZkqrct66bdCHevzEWgmI'
}

data = {
    'date': '2025-01-01',
    'start_time': '23:01:01',
    'pickup_location': 'Champaign, IL',
    'dropoff_location': 'Chicago, IL',
    'open_seats': 1,
    'price': 23.1
}

r = requests.get('http://127.0.0.1:8000/api/past_drives/', headers=headers)
print(r.status_code)

print(r.json())