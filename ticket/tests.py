from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from user.models import User
from flight.models import Flight
from country.models import Country
from city.models import City
from airport.models import Airport
from airline.models import Airline
from airplane.models import Airplane
from luggage.models import Luggage
from .models import Ticket
from faker import Faker

class TicketTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword', is_staff=True)
        
        
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

        self.flight = Flight.objects.create(
            name='Test Flight',
            departure_time=timezone.now() + timedelta(days=1),
            arrival_time=timezone.now() + timedelta(days=1, hours=2),
            airplane=self.airplane,
            source_airport=self.source_airport,
            destination_airport=self.destination_airport,
            luggage=self.luggage
        )

        self.fake = Faker()

    def test_ticket_creation(self):
        ticket = Ticket.objects.create(status=False, flight=self.flight, user=self.user)

        self.assertEqual(Ticket.objects.count(), 1)
        self.assertEqual(ticket.status, False)
        self.assertEqual(ticket.flight, self.flight)
        self.assertEqual(ticket.user, self.user)

    def test_ticket_status_default(self):
        ticket = Ticket.objects.create(flight=self.flight, user=self.user)

        self.assertEqual(ticket.status, False)

    def test_ticket_str_representation(self):
        ticket = Ticket.objects.create(status=False, flight=self.flight, user=self.user)

        expected_str = f'Ticket {ticket.id} - Status: {ticket.status}, Flight: {self.flight}, User: {self.user}'
        self.assertEqual(str(ticket), expected_str)
