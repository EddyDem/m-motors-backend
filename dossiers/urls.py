"""Routes des dossiers"""

from rest_framework.routers import DefaultRouter

from dossiers.views import DossierViewSet

router = DefaultRouter()
router.register("dossiers", DossierViewSet, basename="dossier")

urlpatterns = router.urls
