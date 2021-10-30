from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import CreateOrganisationSerializer,ListOrganisationSerializer,ListMembersSerializer ,GetOrganisationSerializer
from .models import Member, Organisation

class OrganisationViewSet(viewsets.ViewSet):

    def create(self,request):
        user = request.user
        organisation_serializer = CreateOrganisationSerializer(data=request.data)
        organisation_serializer.is_valid(raise_exception=True)
        organisation = organisation_serializer.save()
        admin = Member.objects.create(user=user,organisation=organisation,role="admin")
        admin.save()
        return Response({"status":"success","organistation":organisation_serializer.validated_data})

    def get_orgs(self,request):
        user = request.user
        members = Member.objects.filter(user=user)
        organisations = []
        for i in members:
            organisations += [i.organisation]
        organisations_serializer = ListOrganisationSerializer(organisations,many=True)
        return Response({"status":"success","organisations":organisations_serializer.data})

    def get_org(self,request):
        org_id = request.GET['org_id']
        organisation =  Organisation.objects.get(pk=org_id)
        members = Member.objects.filter(organisation=organisation)
        members_serializer = ListMembersSerializer(members,many=True)
        organisation_serializer = GetOrganisationSerializer(organisation)
        return Response({'status':'success','organisation':organisation_serializer.data,'members':members_serializer.data})
        
