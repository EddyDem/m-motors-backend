"""Dossiers dematerialises et pieces jointes"""

from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models

from dossiers.validators import validate_file_size


class Dossier(models.Model):
    """Dossier d'achat ou de location depose par le client"""

    class Type(models.TextChoices):
        ACHAT = "achat", "Achat"
        LOCATION = "location", "Location"

    class Statut(models.TextChoices):
        DEPOSE = "depose", "Déposé"
        EN_COURS = "en_cours", "En cours"
        VALIDE = "valide", "Validé"
        REFUSE = "refuse", "Refusé"

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="dossiers",
    )
    type = models.CharField("type", max_length=10, choices=Type.choices)
    statut = models.CharField(
        "statut", max_length=10, choices=Statut.choices, default=Statut.DEPOSE
    )
    motif_refus = models.TextField("motif de refus", blank=True)
    cree_le = models.DateTimeField("crée le", auto_now_add=True)
    maj_le = models.DateTimeField("mis à jour le", auto_now=True)

    class Meta:
        ordering = ("-cree_le",)

    def __str__(self):
        return f"Dossier {self.pk} ({self.get_type_display()}) - {self.client}"


def chemin_piece(instance, filename):
    # Range les pieces par dossier : media/dossiers/<id>/<fichier>
    return f"dossiers/{instance.dossier_id}/{filename}"


class Document(models.Model):
    """Piece justificative attachée a un dossier"""

    dossier = models.ForeignKey(
        Dossier,
        on_delete=models.CASCADE,
        related_name="documents",
    )
    fichier = models.FileField(
        "fichier",
        upload_to=chemin_piece,
        validators=(
            FileExtensionValidator(allowed_extensions=("pdf", "jpg", "jpeg", "png")),
            validate_file_size,
        ),
    )
    cree_le = models.DateTimeField("crée le", auto_now_add=True)

    class Meta:
        ordering = ("-cree_le",)

    def __str__(self):
        return f"{self.fichier.name} (dossier {self.dossier_id})"
