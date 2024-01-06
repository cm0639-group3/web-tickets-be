from django.test import TestCase
from cities_light.models import Country
from cities_light.models import City
from .models import Airline

class AirlineTests(TestCase):

    def setUp(self):
        self.country = Country.objects.create(name='Test Country')

    def test_airline_creation(self):
        airline = Airline.objects.create(name='Test Airline', country=self.country)

        self.assertEqual(Airline.objects.count(), 1)
        self.assertEqual(airline.name, 'Test Airline')
        self.assertEqual(airline.country, self.country)

    def test_airline_str_representation(self):
        airline = Airline.objects.create(name='Test Airline', country=self.country)

        expected_str = f'Airline {airline.id} - Name: {airline.name}, Country: {str(self.country)}'
        self.assertEqual(str(airline), expected_str)
