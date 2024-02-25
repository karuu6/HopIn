import requests

headers = {
    'Content-Type': 'application/json;',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA4ODIwNjgwLCJpYXQiOjE3MDg4MjAzODAsImp0aSI6ImJjODA1MzJiODMzNTRlOGFhNmIxY2Q5MmFmM2QwNzhjIiwidXNlcl9pZCI6M30.Bp26AP302LbR7Hg3OSXmuIzEPrekLq-1FOoJkHlTqXk'
}

# data = {
#     'date': '2025-01-01',
#     'start_time': '23:01:01',
#     'pickup_location': 'Champaign, IL',
#     'dropoff_location': 'Chicago, IL',
#     'open_seats': 1,
#     'price': 23.1
# }

data = {
    'username': 'gay',
    'password': 'gay',
}

r = requests.get('http://127.0.0.1:8000/api/past_drives/', headers=headers)
print(r.status_code)

print(r.json())