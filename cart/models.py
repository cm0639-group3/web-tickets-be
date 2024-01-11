from django.db import models
from user.models import User

class Cart(models.Model):
    """
        This model behaves as a cart session.
        It holds the current cart state for a given user,
        until the user completes the order process or leaves the
        cart unattended.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return f'Cart {self.id}'
