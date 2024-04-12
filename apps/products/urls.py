from rest_framework.routers import DefaultRouter

from apps.products.views import ProductAPIViews

router = DefaultRouter()
router.register('products', ProductAPIViews, basename='products')

urlpatterns = router.urls