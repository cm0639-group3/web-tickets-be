from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CityViewSet

router = DefaultRouter()
router.register(r'', CityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
