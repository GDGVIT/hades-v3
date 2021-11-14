from rest_framework import serializers,validators
from django.conf import settings

from organisation.models import Organisation
from .models import Event, Participant
from datetime import datetime, time
from user.models import User
import jwt

key = settings.SECRET_KEY


class CreateParticipantSerializer(serializers.Serializer):
    event_id = serializers.IntegerField(source='event')
    refferal_user = serializers.IntegerField(required=False)
    class Meta:
        model = Participant
        fields = ['event_id']

class JoinParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'
        validators = [validators.UniqueTogetherValidator(Participant.objects.all(),('user','event'),'you are already part of the event')]

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