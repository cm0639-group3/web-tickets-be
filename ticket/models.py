from django.db import models

from flight.models import Flight
from user.models import User


class Ticket(models.Model):
    status = models.BooleanField(default=False)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Ticket {self.id} - Status: {self.status}, Flight: {str(self.flight)}, User: {str(self.user)}"
