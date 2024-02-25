import requests

headers = {
    'Content-Type': 'application/json;',
    'Authorization': 'Bearer '
}

signup_data = {
    'username': '',
    'password': '',
}

login_data = {
    'username': '',
    'password': '',
}

trip_data1 = {
    'date': '2024-03-10',
    'start_time': '11:00:00',
    'pickup_location': 'Champaign, IL',
    'dropoff_location': 'Naperville, IL',
    'open_seats': 3,
    'price': 20,
}

trip_data2 = {
    'date': '2024-03-10',
    'start_time': '15:00:00',
    'pickup_location': 'Savoy, IL',
    'dropoff_location': 'Evanston, IL',
    'open_seats': 1,
    'price': 25,
}

rider = 'john'
driver_names = ['shethh', 'prithvii']

trip_ids = []
for name, trip in zip(driver_names, [trip_data1, trip_data2]):
    signup_json = signup_data.copy()
    signup_json.update({'username': name, 'password': name})
    signup_resp = requests.post('http://127.0.0.1:8000/api/signup/', json=signup_json).json()

    login_json = signup_json
    login_resp = requests.post('http://127.0.0.1:8000/api/token/', json=login_json).json()
    token = login_resp['access']

    cur_headers = headers.copy()
    cur_headers['Authorization'] += token
    post_ride_resp = requests.post('http://127.0.0.1:8000/api/post_trip/', json=trip, headers=cur_headers).json()

    trip_ids.append(post_ride_resp['id'])

signup_json = signup_data.copy()
signup_json.update({'username': rider, 'password': rider})
signup_resp = requests.post('http://127.0.0.1:8000/api/signup/', json=signup_json).json()

login_json = signup_json
login_resp = requests.post('http://127.0.0.1:8000/api/token/', json=login_json).json()
token = login_resp['access']

cur_headers = headers.copy()
cur_headers['Authorization'] += token

req_ride_json = {'trip_id': trip_ids[0]}
req_ride_resp = requests.post('http://127.0.0.1:8000/api/post_hopper_request/', json=req_ride_json, headers=cur_headers).json()

print(req_ride_resp)