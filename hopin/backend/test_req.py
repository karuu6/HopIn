import requests

headers = {
    'Content-Type': 'application/json;',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA4ODI2OTEzLCJpYXQiOjE3MDg4MjY2MTMsImp0aSI6ImIwMWUwY2UwNjU5MzRhNjQ4ZWNiYTQ5MzllMjkxYWQzIiwidXNlcl9pZCI6M30.zdDbM3mrrSRo2wi5QChS5vUqT3wfp8BxlSlkc0ReW78'
}

data = {
    'trip_id': 1,
}

r = requests.post('http://127.0.0.1:8000/api/post_hopper_request/', json=data, headers=headers)
print(r.status_code)

print(r.json())