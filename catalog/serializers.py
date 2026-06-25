"""Serializers du catalogue"""
from rest_framework import serializers

from catalog.models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = (
            "id",
            "marque",
            "modele",
            "motorisation",
            "kilometrage",
            "prix",
            "mode",
            "disponible",
            "cree_le",
        )