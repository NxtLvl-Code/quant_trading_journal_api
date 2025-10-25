from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagViewSet, TradeViewSet, ProfileViewSet

router = DefaultRouter()
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'trades', TradeViewSet, basename='trade')
router.register(r'profiles', ProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
]
