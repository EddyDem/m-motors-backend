"""Vue des dossiers: depot et suivi par le client"""

from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from dossiers.models import Dossier
from dossiers.serializers import DocumentSerializer, DossierSerializer


class DossierViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """Dossiers du client connecte : creation, consultation, suivi du statut"""

    serializer_class = DossierSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Dossier.objects.filter(client=self.request.user)

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

    @action(detail=True, methods=("post",))
    def documents(self, request, pk=None):

        dossier = self.get_object()

        serializer = DocumentSerializer(data=request.FILES)
        serializer.is_valid(raise_exception=True)
        serializer.save(dossier=dossier)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
