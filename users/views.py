from django.shortcuts import render
from rest_framework.generics import ( CreateAPIView,
                                     RetrieveUpdateAPIView)
from django.contrib.auth.models import User
from .serializers import (RegisterSerializer,
                          ProfileSerializer)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Profile
from rest_framework.decorators import api_view
from .permissions import IsOwnerOrStaff
from rest_framework.permissions import IsAuthenticated


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()
        data = serializer.data
        if Token.objects.filter(user=user).exists():
            token = Token.objects.get(user=user)
            data['token'] = token.key
        else:
            data['token'] = 'No token created for this user!!!'

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class ProfileUpdateView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrStaff)


@api_view(['POST'])
def logout(request):
    request.user.auth_token.delete()
    data = {
        'message':'Logged out succesfully!'
    }
    return Response(data, status=status.HTTP_200_OK)