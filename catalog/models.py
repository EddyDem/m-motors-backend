"""Catalogue de véhicules"""

from django.db import models


class Vehicle(models.Model):
    """Véhicule proposé à l'achat ou la location"""

    class Motorisation(models.TextChoices):
        ESSENCE = "essence", "Essence"
        DIESEL = "diesel", "Diesel"
        HYBRIDE = "hybride", "Hybride"
        ELECTRIQUE = "electrique", "Électrique"

    class Mode(models.TextChoices):
        ACHAT = "achat", "Achat"
        LOCATION = "location", "Location"

    marque = models.CharField("marque", max_length=80)
    modele = models.CharField("modèle", max_length=80)
    motorisation = models.CharField(
        "motorisation", max_length=20, choices=Motorisation.choices
    )
    kilometrage = models.PositiveIntegerField("kilométrage", default=0)
    prix = models.DecimalField("prix", max_digits=10, decimal_places=2)
    mode = models.CharField(
        "mode", max_length=20, choices=Mode.choices, default=Mode.ACHAT
    )
    disponible = models.BooleanField("disponible", default=True)
    cree_le = models.DateTimeField("créé le", auto_now_add=True)

    class Meta:
        ordering = ("marque", "modele")

    def __str__(self):
        return f"{self.marque} {self.modele}"
