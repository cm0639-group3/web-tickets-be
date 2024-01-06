from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CountryViewSet

router = DefaultRouter()
router.register(r"", CountryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
