"""Filtres de recherche du catalogue"""

import django_filters

from catalog.models import Vehicle


class VehicleFilter(django_filters.FilterSet):
    marque = django_filters.CharFilter(
        field_name="marque", lookup_expr="icontains", label="Marque"
    )
    modele = django_filters.CharFilter(
        field_name="modele", lookup_expr="icontains", label="Modèle"
    )
    prix_min = django_filters.NumberFilter(
        field_name="prix", lookup_expr="gte", label="Prix minimum"
    )
    prix_max = django_filters.NumberFilter(
        field_name="prix", lookup_expr="lte", label="Prix maximum"
    )
    km_max = django_filters.NumberFilter(
        field_name="kilometrage", lookup_expr="lte", label="Kilométrage maximum"
    )

    class Meta:
        model = Vehicle
        fields = ("motorisation", "mode", "disponible")
