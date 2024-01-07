from rest_framework import viewsets
from rest_framework.response import Response
from .models import Luggage
from rest_framework import status
from .serializers import LuggageSerializer
from .permissions import LuggagePermissions

class LuggageViewSet(viewsets.ModelViewSet):
    queryset = Luggage.objects.all()
    serializer_class = LuggageSerializer
    permission_classes = [LuggagePermissions]
