from sqlite3 import IntegrityError

from cities_light.models import Country
from django.db.utils import IntegrityError as DjangoIntegrityError
from django.test import TestCase
from faker import Faker

from airline.models import Airline

from .models import Airplane


class AirplaneTests(TestCase):
    def setUp(self):
        self.fake = Faker()
        self.country = Country.objects.create(name="Test Country")
        self.airline = Airline.objects.create(name="Test Airline", country=self.country)

    def test_airplane_creation(self):
        random_model_number = self.fake.bothify(text="????####")
        airplane = Airplane.objects.create(
            name="Test Airplane",
            seats=100,
            model_number=random_model_number,
            airline=self.airline,
        )

        self.assertEqual(Airplane.objects.count(), 1)
        self.assertEqual(airplane.name, "Test Airplane")
        self.assertEqual(airplane.seats, 100)
        self.assertEqual(airplane.model_number, random_model_number)
        self.assertEqual(airplane.airline, self.airline)

    def test_airplane_unique_model_number(self):
        random_model_number = self.fake.bothify(text="????####")
        Airplane.objects.create(
            name="Test Airplane 1",
            seats=150,
            model_number=random_model_number,
            airline=self.airline,
        )

        with self.assertRaises((IntegrityError, DjangoIntegrityError, ValueError)):
            Airplane.objects.create(
                name="Test Airplane 2",
                seats=200,
                model_number=random_model_number,
                airline=self.airline,
            )

    def test_airplane_str_representation(self):
        random_model_number = self.fake.bothify(text="????####")
        airplane = Airplane.objects.create(
            name="Test Airplane",
            seats=100,
            model_number=random_model_number,
            airline=self.airline,
        )

        # Check if the __str__ method returns a meaningful representation
        expected_str = f"Airplane {airplane.id} - Name: {airplane.name}, Seats: {airplane.seats}, Model Number: {airplane.model_number}, Airline: {str(airplane.airline)}"
        self.assertEqual(str(airplane), expected_str)
