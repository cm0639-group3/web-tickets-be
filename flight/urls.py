from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FlightViewSet

router = DefaultRouter()
router.register(r"", FlightViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
