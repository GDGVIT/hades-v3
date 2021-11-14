from .models import User
from .serializers import UserSerializer, UserUpdateSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
class UserViewSet(viewsets.ViewSet):

    @action(methods=['get'],detail="Get user data")
    def get_user(self,request):
        serializer = UserSerializer(request.user)
        return Response({'status':'success','user':serializer.data})

    @action(methods=['patch'],detail="Update user data")
    def update_user(self,request):
        serializer = UserUpdateSerializer(request.user,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status':'success','user':serializer.validated_data})