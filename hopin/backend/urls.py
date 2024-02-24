from django.urls import path, include, re_path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from . import views

schema_view = get_schema_view(
   openapi.Info(
      title="Your API",
      default_version='v1',
      description="API documentation for your project",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

swagger_patterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    ]

urlpatterns = [
    path("", views.index, name="index"),
    path('search/', views.search, name='search'),
    path("past_drives", views.past_drives, name="past_drives"),
    path("past_hops", views.past_hops, name="past_hops"),
]

urlpatterns.extend(swagger_patterns)
