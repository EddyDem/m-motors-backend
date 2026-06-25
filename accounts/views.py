"""Vues des comptes: inscription et profil"""

from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from accounts.serializers import RegisterSerializer, UserSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """Inscription d'un nouveau client (accès public)"""

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class MeView(generics.RetrieveUpdateAPIView):
    """Profil de l'utilisateur connecté (lecture et mise à jour)"""

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        """Retourne l'utilisateur connecté"""
        return self.request.user
