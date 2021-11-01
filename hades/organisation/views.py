from rest_framework import serializers, viewsets
import rest_framework.exceptions as exceptions
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import CreateOrganisationSerializer,ListOrganisationSerializer,ListMembersSerializer ,GetOrganisationSerializer, ChangeRoleSerializer, CreateLinkSerializer, JoinLinkSerializer
from .models import Member, Organisation
from user.models import User

class OrganisationViewSet(viewsets.ViewSet):

    @action(methods=['put'],detail="Create organisation")
    def create(self,request):
        user = request.user
        organisation_serializer = CreateOrganisationSerializer(data=request.data)
        organisation_serializer.is_valid(raise_exception=True)
        organisation = organisation_serializer.save()
        admin = Member.objects.create(user=user,organisation=organisation,role="admin")
        admin.save()
        return Response({"status":"success","organistation":organisation_serializer.validated_data})

    @action(methods=['get'],detail="Get list of organisations the user is in")
    def get_orgs(self,request):
        user = request.user
        members = Member.objects.filter(user=user)
        organisations = []
        for i in members:
            organisations += [i.organisation]
        organisations_serializer = ListOrganisationSerializer(organisations,many=True)
        return Response({"status":"success","organisations":organisations_serializer.data})

    @action(methods=['get'],detail="Get details of an organisation")
    def get_org(self,request):
        org_id = request.GET['org_id']
        organisation =  Organisation.objects.get(pk=org_id)
        members = organisation.member.all()
        members_serializer = ListMembersSerializer(members,many=True)
        organisation_serializer = GetOrganisationSerializer(organisation)
        return Response({'status':'success','organisation':organisation_serializer.data,'members':members_serializer.data})
    
    @action(methods=['post'],detail="Change role of a user in an organisation")
    def assign_role(self,request):
        serializer = ChangeRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        role_change_object = serializer.validated_data
        user = request.user
        if user.email == role_change_object['email']:
            raise exceptions.ValidationError('your email cant be the same as the email given')
        organisation = Organisation.objects.filter(pk=role_change_object['org_id']).first()
        admin_member = user.member.filter(organisation=organisation,role='admin').first()
        if not admin_member:
            raise exceptions.PermissionDenied('you are not the admin of this organisation')
        assignee_user = User.objects.filter(email=role_change_object['email']).first()
        member = Member.objects.filter(user=assignee_user,organisation=organisation).first()
        if not member:
            raise serializers.ValidationError('invalid email')
        serializer.update(member,role_change_object)
        return Response({'status':'success','member':role_change_object})
    
    @action(method=['get'],detail="Admin creates organisation join link")
    def create_link(self,request):
        serializer = CreateLinkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = request.user
        organisation = Organisation.objects.filter(pk=data['org_id']).first()
        admin_member = user.member.filter(organisation=organisation,role='admin').first()
        if not admin_member:
            raise exceptions.PermissionDenied('you are not the admin of this organisation')
        link = 'https://' + request.get_host() + '/organisation/join?token=' + serializer.link(data)
        return Response({'status':'succcess','link':link,**data})


    @action(methods=['get'],detail="User joins organisation using link")
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
       
