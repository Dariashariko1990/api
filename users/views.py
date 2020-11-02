from rest_framework import generics, permissions, authentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from users.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Класс для создания нового пользователя"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Класс для создания нового токена при авторизации пользователя"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
