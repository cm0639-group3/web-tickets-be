from django.db import models
from flight.models import Flight
from order.models import Order
from cart.models import Cart

class Ticket(models.Model):
    class TicketType(models.TextChoices):
        SINGLE_TRIP = "SINGLE_TRIP"
        ROUND_TRIP = "ROUND_TRIP"

    status = models.BooleanField(default=False)
    receipt_id = models.CharField(max_length = 12, default="")
    flights = models.ManyToManyField(Flight)

    type = models.CharField(
        max_length=11,
        choices=TicketType,
        default=TicketType.ROUND_TRIP
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.IntegerField(default=1)

    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'Ticket {self.id} - Status: {self.status}, Flight: {str(self.flights)}, User: {str(self.user)}, Type: {str(self.type)}, Price: {str(self.price)}'
