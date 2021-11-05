from django.core.exceptions import NON_FIELD_ERRORS
from rest_framework import exceptions, fields, serializers, validators
from user.models import User

from .models import Member, Organisation

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
    class Meta:
        model =  Member
        fields = ['first_name','email','role']

class ChangeRoleSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    org_id = serializers.IntegerField()
    class Meta:
        model = Member
        fields = ['email','role','org_id']

class JoinMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'
        validators = [validators.UniqueTogetherValidator(Member.objects.all(),('user','organisation'),'member already exists')]
    
class CreateMemberSerializer(serializers.ModelSerializer):
    org_id = serializers.IntegerField(source='organisation')
    class Meta:
        model = Member
        fields = ['org_id','role']