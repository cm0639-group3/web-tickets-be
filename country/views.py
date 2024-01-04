from rest_framework import viewsets
from .models import Country
from .serializers import CountrySerializer
from django.contrib.auth.models import AnonymousUser
from .permissions import CustomPermissions_1
from rest_framework.permissions import  AllowAny, IsAuthenticated , IsAdminUser


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [CustomPermissions_1,]