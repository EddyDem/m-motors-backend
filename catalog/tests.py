"""Tests du catalogue"""

from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from catalog.models import Vehicle

User = get_user_model()


class VehicleModelTestCase(TestCase):
    def test_str(self):
        vehicle = Vehicle.objects.create(
            marque="Toyota",
            modele="Corolla",
            motorisation=Vehicle.Motorisation.ESSENCE,
            prix=Decimal("15000.00"),
        )
        self.assertEqual(str(vehicle), "Toyota Corolla")


class VehicleAPITestCase(APITestCase):
    def setUp(self):
        Vehicle.objects.create(
            marque="Toyota",
            modele="Corolla",
            motorisation=Vehicle.Motorisation.ESSENCE,
            prix=Decimal("15000.00"),
        )

        Vehicle.objects.create(
            marque="Honda",
            modele="Civic",
            motorisation=Vehicle.Motorisation.DIESEL,
            prix=Decimal("18000.00"),
        )

    def test_liste_publique(self):
        response = self.client.get(reverse("vehicle-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)

    def test_filtrage_par_marque(self):
        response = self.client.get(reverse("vehicle-list"), {"marque": "Toyota"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["marque"], "Toyota")


class VehicleAdminActionTestCase(TestCase):

    def setUp(self):
        self.location = Vehicle.objects.create(
            marque="Renault",
            modele="Clio",
            motorisation=Vehicle.Motorisation.ESSENCE,
            prix=Decimal("17000.00"),
            mode=Vehicle.Mode.ACHAT,
        )

    def test_passer_en_location(self):
        Vehicle.objects.filter(pk=self.location.pk).update(mode=Vehicle.Mode.LOCATION)
        self.location.refresh_from_db()
        self.assertEqual(self.location.mode, Vehicle.Mode.LOCATION)


class VehicleAdminWebTestCase(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            email="admin@example.com", password="TestPassword123!"
        )
        self.vehicule = Vehicle.objects.create(
            marque="Renault",
            modele="Clio",
            motorisation=Vehicle.Motorisation.ESSENCE,
            prix=Decimal("17000.00"),
            mode=Vehicle.Mode.ACHAT,
        )

    def test_action_passer_en_location(self):
        self.client.force_login(self.admin)
        self.client.post(
            reverse("admin:catalog_vehicle_changelist"),
            {"action": "passer_en_location", "_selected_action": [self.vehicule.pk]},
        )
        self.vehicule.refresh_from_db()
        self.assertEqual(self.vehicule.mode, Vehicle.Mode.LOCATION)
