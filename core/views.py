from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import User, UserProfile
from core.serializers import LoginSerializer, RegistrationSerializer
from django.contrib.auth import authenticate, login, logout


class RegisterView(CreateAPIView):
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.create_user(**serializer.data)
        return Response({'login': True}, status=status.HTTP_201_CREATED)

    def create_user(self, email, password, company, **kwargs):
        user = User.objects.create_user(email, password)
        UserProfile.objects.create(user=user, company=company)


class LoginView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        user = authenticate(request, username=data['email'], password=data['password'])
        if user is not None:
            login(request, user)
            return Response({'login': True}, status=status.HTTP_200_OK)
        else:
            return Response({'login': False}, status=status.HTTP_403_FORBIDDEN)


class LogoutView(APIView):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            return Response({'login': True}, status=status.HTTP_200_OK)
        else:
            return Response({'login': False}, status=status.HTTP_403_FORBIDDEN)
