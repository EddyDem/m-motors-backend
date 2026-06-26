"""Routes de la souscription"""

from rest_framework.routers import DefaultRouter

from subscriptions.views import ContractViewSet, OptionViewSet

router = DefaultRouter()
router.register("options", OptionViewSet, basename="option")
router.register("contracts", ContractViewSet, basename="contract")

urlpatterns = router.urls
