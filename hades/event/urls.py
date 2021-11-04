from django.urls import path
from .views import EventViewSet

urlpatterns = [
    path('create',EventViewSet.as_view({'put':'create'})), 
    path('create_link',EventViewSet.as_view({'get':'create_link'})),
    path('join',EventViewSet.as_view({'get':'join_event'})),
    path('list_participants',EventViewSet.as_view({'get':'list_participants'})),
]