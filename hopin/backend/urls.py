from django.urls import path, include, re_path, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



urlpatterns = [
    path("past_drives/", views.PastDrives.as_view(), name="past_drives"),
    path("past_hops/", views.PastHops.as_view(), name="past_hops"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('search/', views.Search.as_view(), name='search'),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("post_trip/", views.PostTrip.as_view(), name="post_trip"),
    path("current_hopper_requests/<int:trip_id>/", views.CurrentHopperRequests.as_view(), name="current_hopper_requests"),
    path("hoppers_requests_status", views.HoppersRequestsStatus.as_view(), name="hoppers_requests_status"),
    path('create-hopper-request/<int:trip_id>/', views.AcceptHopperRequest.as_view(), name='accept-hopper-request'),
    path("post_hopper_request/", views.PostHopperRequest.as_view(), name="post_hopper_request"),
    path('decline-hopper-request/<int:hopper_request_id>/', views.DeclineHopperRequest.as_view(), name='decline-hopper-request'),
]
