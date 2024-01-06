from django.db import models
from country.models import Country
# Create your models here.
class Airline(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
        
    def __str__(self):
        return f'Airline {self.id} - Name: {self.name}, Country: {str(self.country)}'