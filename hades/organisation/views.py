from datetime import datetime, timedelta
import re
from rest_framework import serializers, viewsets
import rest_framework.exceptions as exceptions
from rest_framework.response import Response

from .serializers import CreateOrganisationSerializer,UpdateOrganisationSerializer,ListOrganisationSerializer,ListMembersSerializer ,GetOrganisationSerializer, ChangeRoleSerializer,CreateMemberSerializer, JoinMemberSerializer
from .models import Member, Organisation
from utils.link import *

class OrganisationViewSet(viewsets.ViewSet):

    def create(self,request):
        user_inst = request.user
        org_seri = CreateOrganisationSerializer(data=request.data)
        org_seri.is_valid(raise_exception=True)
        org_data = org_seri.validated_data
        org_inst = org_seri.save()
        adm_inst = Member.objects.create(user=user_inst,organisation=org_inst,role="admin")
        adm_inst.save()
        org_data.update({'org_id':org_inst.pk})
        return Response({"status":"success","organistation":org_data})
    
    def update_org(self,request):
       org_seri = UpdateOrganisationSerializer(data=request.data)
       org_seri.is_valid(raise_exception=True) 
       org_data = org_seri.validated_data
       user = request.user
       admin_member = user.member.filter(organisation=org_data['org_id'],role='admin').first()
       if not admin_member:
           raise exceptions.PermissionDenied('you are not the admin of this organisation')
       Organisation.objects.filter(pk=org_data.pop('org_id')).update(**org_data)
       return Response({"status":"success","organisation":org_data})

    def get_orgs(self,request):
        user_inst = request.user
        memb_inst_m = Member.objects.filter(user=user_inst).select_related('organisation')
        org_seri_m = ListOrganisationSerializer(memb_inst_m,many=True)
        return Response({"status":"success","organisations":org_seri_m.data})

    def get_org(self,request):
        org_id = request.GET['org_id']
        if not org_id or org_id.isdigits():
            raise serializers.ValidationError('invalid org_id')
        org_inst =  Organisation.objects.get(pk=org_id)
        memb_inst_m = org_inst.member.all()
        memb_seri_m = ListMembersSerializer(memb_inst_m,many=True)
        org_seri = GetOrganisationSerializer(org_inst)
        return Response({'status':'success','organisation':org_seri.data,'members':memb_seri_m.data})
    
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
        memb_seri = CreateMemberSerializer(data=request.data)
        memb_seri.is_valid(raise_exception=True)
        memb_data = memb_seri.validated_data
        user_inst = request.user
        adm_inst = user_inst.member.filter(organisation=memb_data['organisation'],role='admin').first()
        if not adm_inst:
            raise exceptions.PermissionDenied('you are not the admin of this organisation')
        link = create_link(request,memb_data,datetime.now() + timedelta(minutes=15),'/organisation/join')
        return Response({'status':'succcess',**memb_data,'link':link})

    def join_organisation(self,request):
        user_inst = request.user
        memb_seri = JoinMemberSerializer(data={**verify_token(request),'user':user_inst.pk})
        memb_seri.is_valid(raise_exception=True)
        memb_data = memb_seri.validated_data
        memb_seri.save()
        return Response({'status':'success',**memb_data})
       
