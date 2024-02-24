# HopIn

## _A carpooling app_
HopIn is a carpooling app built with Django and React Native

## Features
- Post rides to and from any location
- Driver/Rider safety verification
- ✨Magic ✨

## Installation

Add the following to your .zshrc or .bashrc and then source it to use google maps api key:

`export GOOGLE_API_KEY=<insert key here>`

HopIn requires [Python](https://python.org/) and [Django](https://www.djangoproject.com/) to run.

Install the dependencies and start the server.

```sh
cd HopIn
pip install -r --use-pep517 requirements.txt
cd hopin
python manage.py migrate
python manage.py runserver
```