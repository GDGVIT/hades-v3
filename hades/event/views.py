import re
from rest_framework import serializers, viewsets
import rest_framework.exceptions as exceptions
from rest_framework.response import Response

from event.models import Event
from .serializers import CreateEventSerializer, JoinParticipantSerializer,CreateParticipantSerializer, ListParticipantsSerializer
from utils.link import *
from .perms import *

class EventViewSet(viewsets.ViewSet):
    
    def create(self,request):
        user_inst = request.user
        event_seri = CreateEventSerializer(data=request.data)
        event_seri.is_valid(raise_exception=True)
        event_data = event_seri.validated_data
        admin = user_inst.member.filter(organisation=event_data['org_id'],role="admin").first()
        if not admin:
            raise exceptions.PermissionDenied('you are not the admin of this organisation')
        event_inst = event_seri.save()
        link_seri = CreateParticipantSerializer(data={'event_id':event_inst.id})
        link_seri.is_valid(raise_exception=True)
        link_data = link_seri.validated_data
        link = create_link(request,link_data,event_data['reg_close_time'],'/event/join')
        event_data.update({'link':link})
        return Response({"status":"success","event":event_data})

    def join_event(self,request):
        user_inst = request.user
        part_seri = JoinParticipantSerializer(data={**verify_token(request),'user':user_inst.pk})
        part_seri.is_valid(raise_exception=True)
        part_data = part_seri.validated_data
        part_seri.save()
        return Response({'status':'success',**part_data})

    def list_participants(self,request):
        user_inst = request.user
        event_id = request.GET.get('event_id')
        if not event_id or not event_id.isdigit():
            raise serializers.ValidationError('event_id is invalid')
        if not has_permission('list_memb',event_id,user_inst):
            raise exceptions.PermissionDenied('you do not have sufficient permissions')
        part_inst_m = Event.objects.get(id=event_id).participants.all().select_related('user')
        part_seri_m = ListParticipantsSerializer(part_inst_m,many=True)
        return Response({'status':'success','participants':part_seri_m.data})

    def list_permission(self,request):
        user_inst = request.user
        event_id = request.GET.get('event_id')
        if not event_id or not event_id.isdigit():
            raise serializers.ValidationError('event_id is invalid')
        role_perm_m = list_permissions(event_id,user_inst)
        return Response({'status':'success','permissions':role_perm_m})