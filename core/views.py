from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import User, UserProfile
from core.serializers import (LanguageSelectorSerializer, LoginSerializer,
                              RegistrationSerializer)


class RegisterView(CreateAPIView):
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.create_user(**serializer.data)
        login(request, user)
        return redirect(reverse('core:chat'))

    def create_user(self, email, password, company, **kwargs):
        user = User.objects.create_user(email, password)
        UserProfile.objects.create(user=user, company=company)
        return user


class LoginView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        user = authenticate(request, username=data['email'], password=data['password'])
        if user is not None:
            login(request, user)
            return redirect(reverse('core:chat'))
        else:
            return Response({'login': False}, status=status.HTTP_403_FORBIDDEN)


class LogoutView(APIView):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            return redirect(reverse('login'))
        else:
            return Response({'login': False}, status=status.HTTP_403_FORBIDDEN)


class LanguageSelectorView(APIView, LoginRequiredMixin):

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = LanguageSelectorSerializer(data=request.data)
        user = self.request.user
        serializer.is_valid(raise_exception=True)
        user.profile.language_code = serializer.data['language_code']
        user.profile.save()
        return Response({'success': True}, status=status.HTTP_200_OK)


class ChatView(LoginRequiredMixin, TemplateView):
    template_name = "hashchat/chat.html"
