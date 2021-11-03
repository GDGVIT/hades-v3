from rest_framework import serializers, viewsets
import rest_framework.exceptions as exceptions
from rest_framework.response import Response
from .serializers import CreateEventSerializer, JoinLinkSerializer,CreateLinkSerializer
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
        event_serializer.save()
        return Response({"status":"success","event":event_data})

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
        participant_object = serializer.validated_data
        user = request.user
        member = user.member.filter(organisation=participant_object['org_id']).first()
        if member:
            raise exceptions.ValidationError('you are already part of the organisation')
        serializer.save(user=user)
        participant_object.pop('exp')
        return Response({'status':'success',**participant_object})

       