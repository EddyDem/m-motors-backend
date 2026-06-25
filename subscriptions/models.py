"""Souscription LOA et options"""

from django.conf import settings
from django.db import models

from catalog.models import Vehicle


class Option(models.Model):
    """Option proposée avec l'abonnement location"""

    class Code(models.TextChoices):
        ASSURANCE = "assurance", "Assurance tous risques"
        ASSISTANCE = "assistance", "Assistance dépannage"
        SAV = "sav", "Entretien et SAV"
        CT = "controle_technique", "Contrôle technique"

    code = models.CharField(max_length=30, choices=Code.choices, unique=True)
    libelle = models.CharField(max_length=80)
    prix_mensuel = models.DecimalField(max_digits=8, decimal_places=2)
    actif = models.BooleanField(default=True)

    class Meta:
        ordering = ("libelle",)

    def __str__(self):
        return f"{self.libelle} ({self.prix_mensuel} €/mois)"
    

class Contract(models.Model):
    """Contrat de location longue durée souscrit par un client."""

    class Statut(models.TextChoices):
        BROUILLON = "brouillon", "Brouillon"
        SOUSCRIT = "souscrit", "Souscrit"

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contrats",
    )
    vehicule = models.ForeignKey(
        Vehicle,
        on_delete=models.PROTECT,
        related_name="contrats",
    )
    options = models.ManyToManyField(Option, blank=True, related_name="contrats")
    duree_mois = models.PositiveIntegerField(default=36)
    loyer_base = models.DecimalField(max_digits=10, decimal_places=2)
    total_mensuel = models.DecimalField(max_digits=10, decimal_places=2)
    total_engagement = models.DecimalField(max_digits=12, decimal_places=2)
    statut = models.CharField(
        max_length=10, choices=Statut.choices, default=Statut.SOUSCRIT
    )
    cree_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-cree_le",)

    def __str__(self):
        return f"Contrat {self.pk} - {self.client} - {self.vehicule}"