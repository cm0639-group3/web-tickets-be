from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer
from .permissions import OrderPermissions

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [OrderPermissions,]
