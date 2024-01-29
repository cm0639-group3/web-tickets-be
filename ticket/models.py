from django.db import models
from flight.models import Flight
from order.models import Order
from cart.models import Cart
from user.models import User
from django.utils import timezone
from luggage.models import Luggage
from decimal import *

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    is_purchased = models.BooleanField(default=False)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    purchased_at = models.DateTimeField(null=True, blank=True)
    luggage = models.ForeignKey(Luggage, on_delete=models.CASCADE, default=1, blank=True)


    @property
    def current_price(self):
        ## an example of price calculation strategy based on remaining seats, it can also been based on remaining days.
        ## also including the luggage price which calculated based on the luggage size and the flight distance.
        price_without_luggage = self.flight.current_price
        luggage_price = 0
        if self.luggage.size != 0:
            luggage_price = self.flight.distance * Decimal(self.luggage.size) / 1000
        return Decimal(price_without_luggage) + luggage_price

    @property
    def is_available(self):
        return self.flight.remaining_seats > 0

    def buy(self):
        if not self.is_purchased:
            self.final_price = self.current_price
            self.is_purchased = True
            self.purchased_at = timezone.now()
            self.flight.buy_ticket()
            self.save()

    def __str__(self):
        return f'Ticket {self.id} , Flight: {str(self.flight)}, User: {str(self.user)}, current_price: {str(self.current_price)}'

