from django.db import models
from airplane.models import Airplane
from airport.models import Airport
from luggage.models import Luggage

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
        if self.remaining_seats < 10:
            return 150.00  # Higher price if fewer seats are remaining
        else:
            return 100.00  # Lower price if more seats are available
        
    def __str__(self):
        return f'Flight {self.id} - Name: {self.name}, Departure: {str(self.departure_time)}, Arrival: {str(self.arrival_time)}, Airplane: {str(self.airplane)}, Source: {str(self.source_airport)}, Destination: {str(self.destination_airport)}'
