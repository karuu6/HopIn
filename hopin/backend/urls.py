from django.urls import path, include, re_path, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



urlpatterns = [
    path("past_drives", views.PastDrives.as_view(), name="past_drives"),
    path("past_hops", views.PastHops.as_view(), name="past_hops"),
    path("current_hopper_requests/<int:trip_id>/", views.CurrentHopperRequests.as_view(), name="current_hopper_requests"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('search/', views.Search.as_view(), name='search'),
    path("signup/", views.SignUp.as_view(), name="signup"),
]
