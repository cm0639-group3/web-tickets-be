from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AirlineViewSet

router = DefaultRouter()
router.register(r'', AirlineViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
