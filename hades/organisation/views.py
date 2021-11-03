from rest_framework import serializers, viewsets
import rest_framework.exceptions as exceptions
from rest_framework.response import Response
from .serializers import CreateOrganisationSerializer,UpdateOrganisationSerializer,ListOrganisationSerializer,ListMembersSerializer ,GetOrganisationSerializer, ChangeRoleSerializer, CreateLinkSerializer, JoinLinkSerializer
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
    
    def update_org(self,request):
       serializer = UpdateOrganisationSerializer(data=request.data)
       serializer.is_valid(raise_exception=True) 
       organisation_data = serializer.validated_data
       user = request.user
       admin_member = user.member.filter(organisation=organisation_data['org_id'],role='admin').first()
       if not admin_member:
           raise exceptions.PermissionDenied('you are not the admin of this organisation')
       Organisation.objects.filter(pk=organisation_data.pop('org_id')).update(**organisation_data)
       return Response({"status":"success","organisation":organisation_data})

    def get_orgs(self,request):
        user = request.user
        organisations = Member.objects.filter(user=user).select_related('organisation')
        organisations_serializer = ListOrganisationSerializer(organisations,many=True)
        return Response({"status":"success","organisations":organisations_serializer.data})

    def get_org(self,request):
        org_id = request.GET['org_id']
        organisation =  Organisation.objects.get(pk=org_id)
        members = organisation.member.all()
        members_serializer = ListMembersSerializer(members,many=True)
        organisation_serializer = GetOrganisationSerializer(organisation)
        return Response({'status':'success','organisation':organisation_serializer.data,'members':members_serializer.data})
    
    def assign_role(self,request):
        serializer = ChangeRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        role_change_object = serializer.validated_data
        user = request.user
        admin_member = user.member.filter(organisation=role_change_object['org_id'],role='admin').first()
        if not admin_member:
            raise exceptions.PermissionDenied('you are not the admin of this organisation')
        if user.email == role_change_object['email']:
            raise exceptions.ValidationError('your email cant be the same as the email given')
        member = Member.objects.filter(user=role_change_object['email'],organisation=role_change_object['org_id']).first()
        if not member:
            raise serializers.ValidationError('invalid email')
        serializer.update(member,role_change_object)
        return Response({'status':'success','member':role_change_object})
    
    def create_link(self,request):
        serializer = CreateLinkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        link_object = serializer.validated_data
        user = request.user
        admin_member = user.member.filter(organisation=link_object['org_id'],role='admin').first()
        if not admin_member:
            raise exceptions.PermissionDenied('you are not the admin of this organisation')
        link = 'https://' + request.get_host() + '/organisation/join?token=' + serializer.link(link_object)
        return Response({'status':'succcess','link':link,**link_object})

    def join_organisation(self,request):
        serializer = JoinLinkSerializer(data={'link':request.GET.get('token')})
        serializer.is_valid(raise_exception=True)
        member_object = serializer.validated_data
        user = request.user
        member = Member.objects.filter(user=user,organisation=member_object['org_id']).first()
        if member:
            raise exceptions.ValidationError('you are already part of the organisation')
        serializer.save(user=user)
        member_object.pop('exp')
        return Response({'status':'success',**member_object})
       
