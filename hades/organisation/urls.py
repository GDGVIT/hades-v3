from django.urls import path
from .views import OrganisationViewSet

urlpatterns = [
    path('create',OrganisationViewSet.as_view({'put':'create'})),
    path('get_orgs',OrganisationViewSet.as_view({'get':'get_orgs'})),
    path('get_org',OrganisationViewSet.as_view({'get':'get_org'})),
    path('create_link',OrganisationViewSet.as_view({'post':'create_link'})),
    path('join',OrganisationViewSet.as_view({'get':'join_organisation'})),
    path('assign_role',OrganisationViewSet.as_view({'post':'assign_role'})),

]