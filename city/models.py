## will use country.models.City instead
# # from django.db import models
# # from country.models import Country

# # # Create your models here.
# # class City(models.Model):
# #     name = models.CharField(max_length=255)
# #     country = models.ForeignKey(Country, on_delete=models.CASCADE)
# #     city = models.ForeignKey('cities_light.City', on_delete=models.SET_NULL, null=True, blank=True)