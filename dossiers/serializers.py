"""Serializers des dossiers"""

from rest_framework import serializers

from dossiers.models import Document, Dossier


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ("id", "fichier", "cree_le")
        read_only_fields = ("id", "cree_le")


class DossierSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Dossier
        fields = (
            "id",
            "type",
            "statut",
            "motif_refus",
            "documents",
            "cree_le",
            "maj_le",
        )
        read_only_fields = ("id", "statut", "motif_refus", "cree_le", "maj_le")
