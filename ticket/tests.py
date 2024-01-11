from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from user.models import User
from role.models import Role
from flight.models import Flight
from cities_light.models import Country, City
from airport.models import Airport
from airline.models import Airline
from airplane.models import Airplane
from luggage.models import Luggage
from .models import Ticket
from faker import Faker

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime
from django.urls import reverse

# class TicketTests(TestCase):

#     def setUp(self):
#         self.flight_country = Country.objects.create(name="Antartida")
#         self.origin_city = City.objects.create(name="One", country=self.flight_country)
#         self.destination_city = City.objects.create(name="Two", country=self.flight_country)

#         self.source_airport = Airport.objects.create(name='Source Airport', code='SRC', city=self.origin_city)
#         self.destination_airport = Airport.objects.create(name='Destination Airport', code='DST', city=self.destination_city)

#         self.airline_country = Country.objects.create(name='Test Country')
#         self.airline = Airline.objects.create(name='Test Airline', country=self.airline_country)

#         self.airplane = Airplane.objects.create(
#             name='Test Airplane',
#             seats=150,
#             model_number='ABC123',
#             airline=self.airline
#         )

#         self.luggage = Luggage.objects.create(name='Test Luggage', size=25, unit='kg')

#         self.flights = [
#             Flight.objects.create(
#                 name='Test Flight',
#                 departure_time=timezone.now() + timedelta(days=1),
#                 arrival_time=timezone.now() + timedelta(days=1, hours=2),
#                 airplane=self.airplane,
#                 source_airport=self.source_airport,
#                 destination_airport=self.destination_airport,
#                 luggage=self.luggage
#             )
#         ]

#         self.fake = Faker()

#     def test_ticket_creation(self):
#         ticket = Ticket.objects.create(status=False, flights=self.flights)

#         self.assertEqual(Ticket.objects.count(), 1)
#         self.assertEqual(ticket.status, False)
#         self.assertEqual(ticket.flights, self.flights)

#     def test_ticket_status_default(self):
#         ticket = Ticket.objects.create(flights=self.flights)

#         self.assertEqual(ticket.status, False)

#     def test_ticket_str_representation(self):
#         ticket = Ticket.objects.create(status=False, flights=self.flights)

#         expected_str = f'Ticket {ticket.id} - Status: {ticket.status}, Flight: {self.flights}'
#         self.assertEqual(str(ticket), expected_str)
