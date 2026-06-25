"""Routes du catalogue"""

from rest_framework.routers import DefaultRouter

from catalog.views import VehicleViewSet

router = DefaultRouter()
router.register("vehicles", VehicleViewSet, basename="vehicle")

urlpatterns = router.urls