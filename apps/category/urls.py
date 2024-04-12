from rest_framework.routers import DefaultRouter

from apps.category.views import CategoryAPIView

router = DefaultRouter()
router.register('category', CategoryAPIView, 'api_categories')

urlpatterns = router.urls