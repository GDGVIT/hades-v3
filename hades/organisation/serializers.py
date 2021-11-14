from django.core.exceptions import NON_FIELD_ERRORS
from rest_framework import exceptions, fields, serializers, validators
from user.models import User

from .models import Member, Organisation, Role

class CreateOrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'

class UpdateOrganisationSerializer(serializers.ModelSerializer):
    org_id = serializers.IntegerField()
    class Meta:
        model = Organisation
        fields = '__all__'
        extra_kwargs = {'name': {'required': False},'logo_pic':{'required':False},'email':{'required':False},'website':{'required':False},'contact_no':{'required':False}}

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
    role = serializers.StringRelatedField(many=True)
    class Meta:
        model =  Member
        fields = ['first_name','email','role']

class AssignRoleSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    org_id = serializers.IntegerField(source='organisation')
    role = serializers.CharField(source='name')
    class Meta:
        model = Role
        fields = ['email','role','org_id']
        validators = []

    def create(self,data):
        role , _ = Role.objects.get_or_create(name=data['name'],organisation_id=data['organisation'])
        return role

class JoinMemberSerializer(serializers.ModelSerializer):
    role = serializers.CharField()
    class Meta:
        model = Member
        fields = ['user','organisation','role']
        validators = [validators.UniqueTogetherValidator(Member.objects.all(),('user','organisation'),'member already exists')]

    def create(self,data):
        role = data.pop('role')
        memb_inst = Member.objects.create(**data)
        Role.objects.get_or_create(name=role,organisation=data['organisation']).members.add(memb_inst)
        return memb_inst
    
class CreateMemberSerializer(serializers.ModelSerializer):
    org_id = serializers.IntegerField(source='organisation')
    role = serializers.CharField()
    class Meta:
        model = Member
        fields = ['org_id','role']

class RemoveMemberSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    org_id = serializers.IntegerField(source='organisation')
    class Meta:
        model = Member
        fields = ['email','org_id']

    def create(self,data):
        return Member.objects.get(user__email=data['email'],organisation=data['organisation']).delete()