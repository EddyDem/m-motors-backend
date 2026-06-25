"""Serializers des comptes"""

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Inscription : valide le mot de passe puis cree le compte"""

    password = serializers.CharField(
        write_only=True, required=True, validators=(validate_password,)
    )

    class Meta:
        model = User
        fields = ("id", "email", "password", "first_name", "last_name", "telephone")

    def create(self, validated_data):
        """Créer un nouvel utilisateur avec un mot de passe haché"""

        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """Profil consultable et modifiable par l'utilisateur connecté"""

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "telephone", "is_staff")
        read_only_fields = ("id", "email", "is_staff")
