from django.db import models

# Create your models here.
class Role():
    name = models.CharField(max_length=50)
    