from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("past_drives", views.past_drives, name="past_drives"),
    path("past_hops", views.past_hops, name="past_hops"),
]
