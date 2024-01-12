from django.test import TestCase
from django.utils import timezone
from airport.models import Airport
from airplane.models import Airplane
from luggage.models import Luggage
from airline.models import Airline
from cities_light.models import Country, City
from faker import Faker
from datetime import timedelta, datetime

from rest_framework.test import APITestCase
from role.models import Role
from user.models import User
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse

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


class FlightAPITests(APITestCase):
    fixtures = ['flight/fixtures/initial_data.json']

    def setUp(self):
        self.role = Role.objects.get_or_create(name="authenticated")
        self.user = User.objects.create_user(
            username='testuser', password='testpassword', is_staff=True, role=self.role[0])
        self.client.force_login(self.user)
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token.access_token))

        self.airplane = Airplane.objects.get(name='AWB A3')

        self.airport_argentina = Airport.objects.get(code='AR3')
        self.airport_belgium = Airport.objects.get(code='BE5')

        self.luggage = Luggage.objects.get(name="small")



        self.flight_data = {
            'name': 'BEL-ARG',
            'departure_time': datetime(2024, 1, 5, 1, 30),
            'arrival_time': datetime(2024, 1, 6, 12, 30),
            'airplane': self.airplane.id,
            'source_airport':self.airport_belgium.id,
            'destination_airport':self.airport_argentina.id,
            'luggage':self.luggage.id,
        }
        self.second_flight_data = {
            'name': 'ARG-BEL',
            'departure_time': datetime(2024, 2, 5, 1, 30),
            'arrival_time': datetime(2024, 2, 6, 12, 30),
            'airplane': self.airplane.id,
            'source_airport':self.airport_argentina.id,
            'destination_airport':self.airport_belgium.id,
            'luggage':self.luggage.id,
        }

    def tearDown(self):
        self.client.logout()

    def test_read_flight_with_filter(self):
        # create flight
        self.client.post(reverse('flight-list'), self.flight_data, format='json')
        # read flight
        response_with_pagination = self.client.get(reverse('flight-list'), {'source_airport__icontains': 'BEL'}, format='json')
        self.assertEqual(response_with_pagination.status_code, status.HTTP_200_OK)
        response = response_with_pagination.data['results']
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]['name'], 'BEL-ARG')

    def test_read_flight_with_pagination(self):
        # create flight
        self.client.post(reverse('flight-list'), self.flight_data, format='json')
        # read flight
        response_with_pagination = self.client.get(reverse('flight-list'), {'source_airport__icontains': 'BEL'}, format='json')

        self.assertEqual(response_with_pagination.status_code, status.HTTP_200_OK)
        self.assertEqual(response_with_pagination.data['count'], 1)
        self.assertEqual(response_with_pagination.data['next'], None)
        self.assertEqual(response_with_pagination.data['previous'], None)
        response = response_with_pagination.data['results']
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]['name'], 'BEL-ARG')

    def test_read_flight_with_ordering(self):
        # create flight
        self.client.post(reverse('flight-list'), self.flight_data, format='json')
        self.client.post(reverse('flight-list'), self.second_flight_data, format='json')
        # read flight

        # Test reading the flight with ordering by name
        response_ordered = self.client.get(reverse('flight-list'), {'ordering': 'name'}, format='json')
        self.assertEqual(response_ordered.status_code, status.HTTP_200_OK)
        self.assertEqual(response_ordered.data['count'], 2)
        self.assertEqual(response_ordered.data['next'], None)
        self.assertEqual(response_ordered.data['previous'], None)

        response = response_ordered.data['results']
        self.assertEqual(response[0]['name'], 'ARG-BEL')
        self.assertEqual(response[1]['name'], 'BEL-ARG')

    def test_partial_update_flight(self):
        # create flight
        self.client.post(reverse('flight-list'), self.flight_data, format='json')
        # read flight
        response_filter = self.client.get(
            reverse('flight-list'), {'name__icontains': 'Ponte'}, format='json')
        flight = response_filter.data['results'][0]

        # update
        updated_data =  {'name': 'BEL-ARG.2024-01'}
        response = self.client.patch(reverse('flight-detail', args=[flight['id']]), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Flight.objects.get().name, 'BEL-ARG.2024-01')

    def test_delete_flight(self):
        # create flight
        self.client.post(reverse('flight-list'), self.flight_data, format='json')
        # read flight
        response_filter = self.client.get(
            reverse('flight-list'), {'name__icontains': 'BEL-ARG'}, format='json')
        flight = response_filter.data['results'][0]

        # delete flight
        response = self.client.delete(reverse('flight-detail', args=[flight['id']]), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Flight.objects.count(), 0)
