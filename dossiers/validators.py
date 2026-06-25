"""Validateurs des pieces de dossier"""

from django.core.exceptions import ValidationError

TAILLE_MAX_MO = 5


def validate_file_size(value):
    """Limite de taille de fichier"""
    if value.size > TAILLE_MAX_MO * 1024 * 1024:
        raise ValidationError(
            f"La taille du fichier ne doit pas dépasser {TAILLE_MAX_MO} Mo."
        )
