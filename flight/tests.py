from django.test import TestCase
from django.utils import timezone
from airport.models import Airport
from airplane.models import Airplane
from luggage.models import Luggage
from airline.models import Airline
from city.models import City
from country.models import Country
from faker import Faker
from datetime import timedelta
from .models import Flight

class FlightTests(TestCase):

    def setUp(self):
        self.flight_country = Country.objects.create(name="Antartida")
        self.origin_city = City.objects.create(name="One", country=self.flight_country)
        self.destination_city = City.objects.create(name="Two", country=self.flight_country)

        self.source_airport = Airport.objects.create(name='Source Airport', code='SRC', city=self.origin_city)
        self.destination_airport = Airport.objects.create(name='Destination Airport', code='DST', city=self.destination_city)

        self.airline_country = Country.objects.create(name='Test Country')
        self.airline = Airline.objects.create(name='Test Airline', country=self.airline_country)

        self.airplane = Airplane.objects.create(
            name='Test Airplane',
            seats=150,
            model_number='ABC123',
            airline=self.airline 
        )

        self.luggage = Luggage.objects.create(name='Test Luggage', size=25, unit='kg')

        self.fake = Faker()

    def test_flight_creation(self):
        flight = Flight.objects.create(
            name='Test Flight',
            departure_time=timezone.now(),
            arrival_time=timezone.now() + timedelta(hours=2),
            airplane=self.airplane,
            source_airport=self.source_airport,
            destination_airport=self.destination_airport,
            luggage=self.luggage
        )

        self.assertEqual(Flight.objects.count(), 1)
        self.assertEqual(flight.name, 'Test Flight')
        self.assertIsNotNone(flight.departure_time)
        self.assertIsNotNone(flight.arrival_time)
        self.assertEqual(flight.airplane, self.airplane)
        self.assertEqual(flight.source_airport, self.source_airport)
        self.assertEqual(flight.destination_airport, self.destination_airport)
        self.assertEqual(flight.luggage, self.luggage)

    def test_flight_arrival_time_validation(self):
        with self.assertRaises(ValueError):
            Flight.objects.create(
                name='Test Flight',
                departure_time=timezone.now(),
                arrival_time=timezone.now() - timedelta(hours=1),
                airplane=self.airplane,
                source_airport=self.source_airport,
                destination_airport=self.destination_airport,
                luggage=self.luggage
            )

    def test_flight_str_representation(self):
        flight = Flight.objects.create(
            name=self.fake.company(),
            departure_time=timezone.now(),
            arrival_time=timezone.now() + timedelta(hours=2),
            airplane=self.airplane,
            source_airport=self.source_airport,
            destination_airport=self.destination_airport,
            luggage=self.luggage
        )

        expected_str = f'Flight {flight.id} - Name: {flight.name}, Departure: {flight.departure_time}, Arrival: {flight.arrival_time}, Airplane: {self.airplane}, Source: {self.source_airport}, Destination: {self.destination_airport}, Luggage: {self.luggage}'
        self.assertEqual(str(flight), expected_str)
