from django.db import models

from user.models import User


# Create your models here.
class Notification:
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
