from django.db import models

from flight.models import Flight
from user.models import User


# Create your models here.
class Ticket(models.Model):
    status = models.BooleanField(default=False)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
