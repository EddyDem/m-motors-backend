"""Vues de la souscription LOA"""

from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from subscriptions.models import Contract, Option
from subscriptions.pricing import calculer_devis
from subscriptions.serializers import (
    ContractInputSerializer,
    ContractSerializer,
    OptionSerializer,
)


class OptionViewSet(viewsets.ReadOnlyModelViewSet):
    """Catalogue des options actives"""

    queryset = Option.objects.filter(actif=True)
    serializer_class = OptionSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    

class ContractViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """Souscriptions du client connecté: devis, création, suivi"""

    serializer_class = ContractSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Contract.objects.filter(client=self.request.user)
    
    @action(detail=False, methods=("post",))
    def devis(self, request):
        """Calcule le prix sans rien enregistrer (aperçu)"""
        entree = ContractInputSerializer(data=request.data)
        entree.is_valid(raise_exception=True)
        recap = calculer_devis(
            entree.validated_data["vehicule"],
            entree.validated_data.get("options", []),
            entree.validated_data["duree_mois"],
        )
        return Response(recap)
    
    def create(self, request, *args, **kwargs):
        """Souscrit : fige les montants calculés dans le contrat"""
        entree = ContractInputSerializer(data=request.data)
        entree.is_valid(raise_exception=True)
        vehicule = entree.validated_data["vehicule"]
        options = entree.validated_data.get("options", [])
        duree = entree.validated_data["duree_mois"]

        recap = calculer_devis(vehicule, options, duree)
        contrat = Contract.objects.create(
            client=request.user,
            vehicule=vehicule,
            duree_mois=duree,
            loyer_base=recap["loyer_base"],
            total_mensuel=recap["total_mensuel"],
            total_engagement=recap["total_engagement"],
        )
        contrat.options.set(options)

        sortie = ContractSerializer(contrat)
        return Response(sortie.data, status=status.HTTP_201_CREATED)