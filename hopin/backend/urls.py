from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:ride_id>/", views.view_ride, name="view_ride"),
]
