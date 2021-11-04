import re
from rest_framework import serializers, viewsets
import rest_framework.exceptions as exceptions
from rest_framework.response import Response

from event.models import Event
from .serializers import CreateEventSerializer, JoinLinkSerializer,CreateLinkSerializer, ListParticipantsSerializer
from organisation.models import Member

class EventViewSet(viewsets.ViewSet):
    
    def create(self,request):
        user = request.user
        event_serializer = CreateEventSerializer(data=request.data)
        event_serializer.is_valid(raise_exception=True)
        event_data = event_serializer.validated_data
        admin = user.member.filter(organisation=event_data['org_id'],role="admin").first()
        if not admin:
            raise exceptions.PermissionDenied('you are not the admin of this organisation')
        event_object = event_serializer.save()
        link_serializer = CreateLinkSerializer(data={'event_id':event_object.id,'exp':event_object.reg_close_time})
        link_serializer.is_valid(raise_exception=True)
        link = 'https://' + request.get_host() + '/event/join?token=' + link_serializer.validated_data['link']
        event_data.update({'link':link})
        return Response({"status":"success","event":event_data})

    def create_link(self,request):
        serializer = CreateLinkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        link_object = serializer.validated_data
        user = request.user
        admin_member = user.member.filter(organisation=link_object['org_id'],role='admin').first()
        if not admin_member:
            raise exceptions.PermissionDenied('you are not the admin of this organisation')
        link = 'https://' + request.get_host() + '/event/join?token=' + serializer.validated_data['link']
        return Response({'status':'succcess','link':link})

    def join_event(self,request):
        serializer = JoinLinkSerializer(data={'link':request.GET.get('token')})
        serializer.is_valid(raise_exception=True)
        participant_object = serializer.validated_data
        user = request.user
        member = user.participant.filter(event=participant_object['event_id']).first()
        if member:
            raise exceptions.ValidationError('you are already part of the event')
        serializer.save(user=user)
        participant_object.pop('exp')
        return Response({'status':'success',**participant_object})

    def list_participants(self,request):
        user = request.user
        event_id = request.GET.get('event_id')
        if not event_id or not event_id.isdigit():
            raise serializers.ValidationError('event_id is invalid')
        event = Event.objects.get(pk=int(event_id))
        if not event:
            raise serializers.ValidationError('event does not exist')
        member = user.member.filter(organisation=event.organisation).first()
        if not member:
            raise exceptions.PermissionDenied('you are not a member of this organisation')
        participants = event.participants.all().select_related('user')
        serializer = ListParticipantsSerializer(participants,many=True)
        return Response({'status':'success','participants':serializer.data})

