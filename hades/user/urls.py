from django.urls import path
from user.auth_views import EmailAuthViewSet

urlpatterns = [
    path("email/login/",EmailAuthViewSet.as_view({'post':'login'})),
    path("email/register/",EmailAuthViewSet.as_view({'post':'register'}))
]