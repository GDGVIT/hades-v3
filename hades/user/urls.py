from django.urls import path
from user.views import UserViewSet

urlpatterns = [
    path("",UserViewSet.as_view({'get':'get_user'})),
    path("update/",UserViewSet.as_view({'patch':'update_user'}))
]