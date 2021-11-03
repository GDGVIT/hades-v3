from django.urls import path
from .views import EventViewSet

urlpatterns = [
    path('create',EventViewSet.as_view({'put':'create'})), 
]