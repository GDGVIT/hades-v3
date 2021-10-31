from rest_framework import fields, serializers, validators

from user.models import User

from .models import Member, Organisation

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