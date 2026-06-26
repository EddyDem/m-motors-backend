"""Tests de la souscription LOA"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from catalog.models import Vehicle
from subscriptions.models import Contract, Option
from subscriptions.pricing import calculer_devis

User = get_user_model()


class PricingTestCase(APITestCase):
    """Logique métier de calcul du prix"""

    def setUp(self):
        self.vehicule = Vehicle.objects.create(
            marque="Renault",
            modele="Megane",
            motorisation=Vehicle.Motorisation.ESSENCE,
            prix=Decimal("20000.00"),
            mode=Vehicle.Mode.LOCATION,
        )
        self.assurance = Option.objects.get(code="assurance")

    def test_devis_sans_option(self):
        recap = calculer_devis(self.vehicule, [], 36)

        self.assertEqual(recap["loyer_base"], Decimal("300.00"))
        self.assertEqual(recap["total_mensuel"], Decimal("300.00"))
        self.assertEqual(recap["total_engagement"], Decimal("10800.00"))

    def test_devis_avec_option(self):
        recap = calculer_devis(self.vehicule, [self.assurance], 36)

        self.assertEqual(recap["total_mensuel"], Decimal("339.00"))
        self.assertEqual(recap["total_engagement"], Decimal("12204.00"))

    def test_devis_refuse_vehicule_en_vente(self):
        self.vehicule.mode = Vehicle.Mode.ACHAT
        self.vehicule.save()
        with self.assertRaises(ValueError):
            calculer_devis(self.vehicule, [], 36)

    def test_devis_refuse_duree_invalide(self):
        with self.assertRaises(ValueError):
            calculer_devis(self.vehicule, [], 0)


class ContractApiTestCase(APITestCase):
    """API de souscription"""

    def setUp(self):
        self.user = User.objects.create_user(
            email="client@example.com", password="TestPassword123!"
        )
        self.autre = User.objects.create_user(
            email="autre@example.com", password="TestPassword123!"
        )
        self.vehicule = Vehicle.objects.create(
            marque="Peugeot",
            modele="208",
            motorisation=Vehicle.Motorisation.ESSENCE,
            prix=Decimal("18000.00"),
            mode=Vehicle.Mode.LOCATION,
        )
        self.assurance = Option.objects.get(code="assurance")

    def test_devis_exige_authentification(self):
        response = self.client.post(reverse("contract-devis"), {}, format="json")
        self.assertEqual(response.status_code, 401)

    def test_souscription_fige_les_montants(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(
            reverse("contract-list"),
            {"vehicule": self.vehicule.pk, "options": [self.assurance.pk]},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        contrat = Contract.objects.get(pk=response.data["id"])

        self.assertEqual(contrat.total_mensuel, Decimal("309.00"))

    def test_client_ne_voit_que_ses_contrats(self):
        Contract.objects.create(
            client=self.autre,
            vehicule=self.vehicule,
            loyer_base=Decimal("270.00"),
            total_mensuel=Decimal("270.00"),
            total_engagement=Decimal("9720.00"),
        )
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse("contract-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 0)
