from rest_framework import serializers
from django.conf import settings

from organisation.models import Organisation
from .models import Event, Participant
from datetime import datetime, time
from user.models import User
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
        exclude = ['user','event']
    
    def validate(self, data):
        try:
            link = jwt.decode(data['link'],key,'HS256')
        except Exception as e:
            print(e)
            raise serializers.ValidationError('invalid link')
        
        return link

    def create(self, validated_data):
        event = Event(pk=validated_data['event_id'])
        refferal = validated_data.get('refferal_user')
        user = validated_data['user']
        participant = Participant(event=event,user=user)
        participant.save()
        return participant

class CreateEventSerializer(serializers.ModelSerializer):
    org_id = serializers.IntegerField()
    def validate(self, data):
        timezone = data['start_time'].tzinfo
        if timezone != data['reg_close_time'].tzinfo or timezone != data['end_time'].tzinfo:
            raise serializers.ValidationError('timezones of timestamps do not match')
        elif datetime.now(tz=timezone) >= data['start_time']:
            raise serializers.ValidationError('event start time cant be before now')
        elif datetime.now(tz=timezone) >= data['reg_close_time']:
            raise serializers.ValidationError('registration close time cant be before now')
        elif data['start_time'] >= data['end_time']:
            raise serializers.ValidationError('event start time cant be later than event end time')
        elif data['reg_close_time'] >= data['end_time']:
            raise serializers.ValidationError('registration close time cant be after the event end time')
        return data

    def create(self,data):
        data.update({'organisation':Organisation(pk=data.pop('org_id'))})
        event = Event(**data)
        event.save()
        return event
    class Meta:
        model = Event
        exclude = ['organisation']

class ListParticipantsSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    phone_no = serializers.CharField(source='user.phone_no')
    class Meta:
        model = Participant
        exclude = ['event','user']