from rest_framework.routers import DefaultRouter

from apps.billing.views import BillingAPIView

router = DefaultRouter()
router.register('billings', BillingAPIView, "api_billings")

urlpatterns = router.urls