"""Vues du catalogue : recherche publique, lecture seule."""

from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from catalog.filters import VehicleFilter
from catalog.models import Vehicle
from catalog.serializers import VehicleSerializer


class VehicleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = (AllowAny,)
    filterset_class = VehicleFilter
