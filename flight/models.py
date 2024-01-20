from django.db import models
from airplane.models import Airplane
from airport.models import Airport
from luggage.models import Luggage
import decimal

class Flight(models.Model):
    name = models.CharField(max_length = 255)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    source_airport = models.ForeignKey(
        Airport, on_delete=models.CASCADE , related_name='source_airport')
    destination_airport = models.ForeignKey(
        Airport, on_delete=models.CASCADE , related_name='destination_airport')
    
    remaining_seats = models.IntegerField(default=10)
    seats = models.IntegerField(default=10)
    distance = models.IntegerField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2 , null =True)

    def clean(self):
        if self.departure_time and self.arrival_time and self.departure_time >= self.arrival_time:
            raise ValueError("Departure time must be before arrival time.")

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the object is being created
            self.seats = self.airplane.seats
            self.remaining_seats = self.airplane.seats
        self.clean()
        super().save(*args, **kwargs)

    def buy_ticket(self):
        if self.remaining_seats > 0:
            self.remaining_seats -= 1
            self.save()

    @property
    def current_price(self):
        ## an example of price calculation strategy based on remaining seats, it can also been based on remaining days.
        ## this price without luggage
        if self.base_price:
            remaining_fricion = float(self.remaining_seats / self.seats)
            additional_price = self.base_price * decimal.Decimal((1-remaining_fricion)**4)
            return self.base_price + additional_price
            ## additional price based on remaining seats friction such as base price multiplied by for example f(remaining_fricion) = (1-remaining_fricion)**4
            ## f(x) = (1-x) ^ 4 {y: [0-1], x: [0-1]}
            ## f(1) = 0, f(0.75) = 0.003, f(0.5) = 0.0625, f(0.4) = 0.129, f(0.3) = 0.24, f(0.2) = 0.40, f(0.1) = 0.65, f(0.05) = 0.81, f(0) = 1
        else:
            ## any other calculation strategy if based price not available (however, this not possible because create flight required based_price)
            if self.remaining_seats < 10:
                return 150.00  # Higher price if fewer seats are remaining
            else:
                return 100.00  # Lower price if more seats are available
        
    @property
    def is_available(self):
        return self.remaining_seats > 0
        
    def __str__(self):
        return f'Flight {self.id} - Name: {self.name}, Departure: {str(self.departure_time)}, Arrival: {str(self.arrival_time)}, Airplane: {str(self.airplane)}, Source: {str(self.source_airport)}, Destination: {str(self.destination_airport)}'
