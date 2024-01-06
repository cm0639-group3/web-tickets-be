from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AirportViewSet

router = DefaultRouter()
router.register(r"", AirportViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
