from rest_framework import serializers
from django.conf import settings

from organisation.models import Organisation
from .models import Event, Participant
from datetime import datetime
import jwt

key = settings.SECRET_KEY


class CreateLinkSerializer(serializers.Serializer):
    event_id = serializers.IntegerField()
    refferal_user = serializers.IntegerField(required=False)
    exp = serializers.DateTimeField()

    def validate(self, data):
        data.update({'link':jwt.encode({**data},key,'HS256')})
        return data

class JoinLinkSerializer(serializers.ModelSerializer):
    link = serializers.CharField()
    class Meta:
        model = Participant
        fields = '__all__'
        read_only_fields = ['organisation','user','role']
    
    def validate(self, data):
        try:
            link = jwt.decode(data['link'],key,'HS256')
        except:
            raise serializers.ValidationError('invalid link')
        
        return link

    def create(self, validated_data):
        event = validated_data['event_id']
        refferal = validated_data['refferal_user']
        user = validated_data['user']
        participant = Participant(event=event,user=user)
        participant.save()
        return participant

class CreateEventSerializer(serializers.ModelSerializer):
    org_id = serializers.IntegerField()
    link = CreateLinkSerializer()
    def validate(self, data):
        timezone = data['start_time'].timez
        if timezone != data['reg_close_time'].timez or timezone != data['end_time']:
            raise serializers.ValidationError('timezones of timestamps do not match')
        elif datetime.now(tz=timezone) >= data['start_time']:
            raise serializers.ValidationError('event start time cant be before now')
        elif data['start_time'] >= data['end_time']:
            raise serializers.ValidationError('event start time cant be later than event end time')
        elif data['reg_close_time'] >= data['end_time']:
            raise serializers.ValidationError('registration close time cant be after the event end time')
        return data

    def create(self,data):
        data.update({'organisation':data.pop('org_id')})
        event = Event(**data)
        event.save()
        return event
    class Meta:
        model = Event
        exclude = ['organisation']
