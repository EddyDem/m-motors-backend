"""Serializers de la souscription"""

from rest_framework import serializers

from catalog.models import Vehicle
from subscriptions.models import Contract, Option


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ("id", "code", "libelle", "prix_mensuel")
        

class ContractInputSerializer(serializers.Serializer):
    """Entrée d'un devis ou d'une souscription."""

    vehicule = serializers.PrimaryKeyRelatedField(
        queryset=Vehicle.objects.filter(mode=Vehicle.Mode.LOCATION, disponible=True)
    )
    options = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Option.objects.filter(actif=True), required=False
    )
    duree_mois = serializers.IntegerField(min_value=1, default=36)
    

class ContractSerializer(serializers.ModelSerializer):
    """Représentation d'un contrat (récapitulatif)."""

    options = OptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Contract
        fields = (
            "id",
            "vehicule",
            "options",
            "duree_mois",
            "loyer_base",
            "total_mensuel",
            "total_engagement",
            "statut",
            "cree_le",
        )
        read_only_fields = fields