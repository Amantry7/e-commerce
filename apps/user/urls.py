from rest_framework.routers import DefaultRouter
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.user.views import UserViewsSet


router = DefaultRouter()
router.register('users', UserViewsSet, basename='api_users')

urlpatterns=[
    path('login/', TokenObtainPairView.as_view(), name='api_login'),
    path('refresh/', TokenRefreshView.as_view(), name='api_refresh')
]

urlpatterns += router.urls