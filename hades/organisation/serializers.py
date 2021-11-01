from rest_framework import exceptions, fields, serializers, validators
from django.conf import settings
from user.models import User

from .models import Member, Organisation
import jwt
from datetime import datetime, timedelta, timezone

key = settings.SECRET_KEY
class CreateOrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'

class GetOrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'

class ListOrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ['id','name','logo_pic']

class ListMembersSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    email = serializers.EmailField(source='user.email')
    class Meta:
        model =  Member
        fields = ['first_name','email','role']

class ChangeRoleSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    org_id = serializers.IntegerField()
    class Meta:
        model = Member
        fields = ['email','role','org_id']

class CreateLinkSerializer(serializers.Serializer):
    org_id = serializers.IntegerField()
    role = serializers.CharField(max_length=10)

    def link(self, obj):
        link = jwt.encode({'org_id':obj['org_id'],'role':obj['role'],'exp':datetime.now(tz=timezone.utc) + timedelta(minutes=15)},key,'HS256')
        return link

class JoinLinkSerializer(serializers.ModelSerializer):
    link = serializers.CharField()
    class Meta:
        model = Member
        fields = '__all__'
        read_only_fields = ['organisation','user','role']
    
    def validate(self, data):
        try:
            link = jwt.decode(data['link'],key,'HS256')
        except:
            raise serializers.ValidationError('invalid link')
        
        return link

    def create(self, validated_data):
        organisation = validated_data['org_id']
        role = validated_data['role']
        user = validated_data['user']
        member = Member(organisation=organisation,user=user,role=role)
        member.save()
        return member