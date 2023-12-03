from django.db import models
from user.models import User
from flight.models import Flight
# Create your models here.
class Order():
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)