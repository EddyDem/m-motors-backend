"""Tests du catalogue"""

from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from catalog.models import Vehicle


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
