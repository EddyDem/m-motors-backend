"""Tests des comptes"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

User = get_user_model()


class RegisterViewTestCase(APITestCase):
    """Tests pour l'inscription"""

    def test_inscription_cree_un_compte(self):
        response = self.client.post(
            reverse("register"),
            {
                "email": "test@example.com",
                "password": "TestPassword123!",
                "first_name": "Jean",
                "last_name": "Client",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(email="test@example.com").exists())

    def test_mot_de_passe_trop_faible_refusee(self):
        response = self.client.post(
            reverse("register"),
            {
                "email": "faible@example.com",
                "password": "123",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)


class AuthTestCase(APITestCase):
    """Tests pour l'authentification"""

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="TestPassword123!",
        )

    def test_login_retourne_des_tokens(self):
        response = self.client.post(
            reverse("login"),
            {
                "email": "test@example.com",
                "password": "TestPassword123!",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_me_exige_authentification(self):
        response = self.client.get(reverse("me"))
        self.assertEqual(response.status_code, 401)

    def test_me_retourne_le_profil_utilisateur(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("me"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], "test@example.com")
