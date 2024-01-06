from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from role.models import Role
from user.models import User

from .models import Luggage


class LuggageTests(APITestCase):
    def setUp(self):
        self.role = Role.objects.get_or_create(name="authenticated")
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            is_staff=True,
            role=self.role[0],
        )
        self.client.force_login(self.user)
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + str(self.token.access_token)
        )
        self.luggage_data = {"name": "Test Luggage", "size": 25, "unit": "kg"}

    def test_create_luggage(self):
        response = self.client.post(
            reverse("luggage-list"), self.luggage_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Luggage.objects.count(), 1)
        self.assertEqual(Luggage.objects.get().name, "Test Luggage")

    def test_read_luggage(self):
        luggage = Luggage.objects.create(name="Test Luggage", size=25, unit="kg")
        response = self.client.get(
            reverse("luggage-detail", args=[luggage.id]), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Luggage")

    def test_update_luggage(self):
        luggage = Luggage.objects.create(name="Test Luggage", size=25, unit="kg")
        updated_data = {"name": "Updated Luggage", "size": 30, "unit": "lbs"}
        response = self.client.put(
            reverse("luggage-detail", args=[luggage.id]), updated_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Luggage.objects.get().name, "Updated Luggage")

    def test_delete_luggage(self):
        luggage = Luggage.objects.create(name="Test Luggage", size=25, unit="kg")
        response = self.client.delete(
            reverse("luggage-detail", args=[luggage.id]), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Luggage.objects.count(), 0)
