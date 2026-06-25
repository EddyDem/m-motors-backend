"""Tests des dossiers"""

import tempfile

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from rest_framework.test import APITestCase
from django.core.exceptions import ValidationError
from django.test import TestCase

from dossiers.models import Dossier

User = get_user_model()


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class DossierTestCase(APITestCase):
    def setUp(self):
        self.client_user = User.objects.create_user(
            email="client@example.com", password="TestPassword123!"
        )
        self.autre = User.objects.create_user(
            email="autre@example.com", password="TestPassword123!"
        )

    def test_creation_exige_authentification(self):
        response = self.client.post(
            reverse("dossier-list"), {"type": "achat"}, format="json"
        )
        self.assertEqual(response.status_code, 401)

    def test_client_cree_un_dossier(self):
        self.client.force_authenticate(self.client_user)
        response = self.client.post(
            reverse("dossier-list"), {"type": "achat"}, format="json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["statut"], "depose")

    def test_client_ne_voit_que_ses_dossiers(self):
        Dossier.objects.create(client=self.autre, type="achat")
        self.client.force_authenticate(self.client_user)
        response = self.client.get(reverse("dossier-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 0)

    def test_upload_document(self):
        self.client.force_authenticate(self.client_user)
        dossier = Dossier.objects.create(client=self.client_user, type="achat")
        fichier = SimpleUploadedFile(
            "piece.pdf", b"%PDF-1.4 contenu", content_type="application/pdf"
        )
        url = reverse("dossier-documents", args=(dossier.pk,))
        response = self.client.post(url, {"fichier": fichier}, format="multipart")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(dossier.documents.count(), 1)

    def test_upload_mauvais_type_refuse(self):
        self.client.force_authenticate(self.client_user)
        dossier = Dossier.objects.create(client=self.client_user, type="achat")
        fichier = SimpleUploadedFile(
            "virus.exe", b"contenu", content_type="application/octet-stream"
        )
        url = reverse("dossier-documents", args=(dossier.pk,))
        response = self.client.post(url, {"fichier": fichier}, format="multipart")
        self.assertEqual(response.status_code, 400)

class DossierValidationTestCase(TestCase):

    def setUp(self):
        self.client_user = User.objects.create_user(
            email="client@example.com", password="TestPassword123!"
        )
        self.dossier = Dossier.objects.create(
            client=self.client_user, type=Dossier.Type.ACHAT
        )

    def test_valider_passe_au_statut_valide(self):
        self.dossier.refuser("Pièce illisible")
        self.dossier.valider()
        self.assertEqual(self.dossier.statut, Dossier.Statut.VALIDE)
        self.assertEqual(self.dossier.motif_refus, "")

    def test_refuser_enregistre_le_motif(self):
        self.dossier.refuser("Justificatif manquant")
        self.assertEqual(self.dossier.statut, Dossier.Statut.REFUSE)
        self.assertEqual(self.dossier.motif_refus, "Justificatif manquant")

    def test_refuser_sans_motif_leve_une_erreur(self):
        with self.assertRaises(ValidationError):
            self.dossier.refuser("   ")
        self.dossier.refresh_from_db()
        self.assertEqual(self.dossier.statut, Dossier.Statut.DEPOSE)