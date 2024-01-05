from rest_framework import viewsets
from .models import Role
from .serializers import RoleSerializer
from rest_framework.permissions import  AllowAny, IsAuthenticated , IsAdminUser

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdminUser,]