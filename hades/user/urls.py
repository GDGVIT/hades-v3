from django.urls import path
from user.auth_views import EmailAuthViewSet,GoogleAuthViewSet

urlpatterns = [
    path("email/login/",EmailAuthViewSet.as_view({'post':'login'})),
    path("email/register/",EmailAuthViewSet.as_view({'post':'register'})),
    path("google/login/",GoogleAuthViewSet.as_view({'post':'login'})),
    path("google/register/",GoogleAuthViewSet.as_view({'post':'register'}))
]