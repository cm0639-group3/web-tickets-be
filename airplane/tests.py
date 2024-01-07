from sqlite3 import IntegrityError
from django.db.utils import IntegrityError as DjangoIntegrityError
from rest_framework.test import APITestCase
from role.models import Role
from user.models import User
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.test import TestCase
from airline.models import Airline
from cities_light.models import Country
from faker import Faker
from django.urls import reverse

from .models import Airplane

class AirplaneTests(TestCase):

    def setUp(self):
        self.fake = Faker()
        self.country = Country.objects.create(name='Test Country')
        self.airline = Airline.objects.create(name='Test Airline', country=self.country)

    def test_airplane_creation(self):
        random_model_number = self.fake.bothify(text='????####')
        airplane = Airplane.objects.create(name='Test Airplane', seats=100, model_number=random_model_number, airline=self.airline)

        self.assertEqual(Airplane.objects.count(), 1)
        self.assertEqual(airplane.name, 'Test Airplane')
        self.assertEqual(airplane.seats, 100)
        self.assertEqual(airplane.model_number, random_model_number)
        self.assertEqual(airplane.airline, self.airline)

    def test_airplane_unique_model_number(self):
        random_model_number = self.fake.bothify(text='????####')
        Airplane.objects.create(name='Test Airplane 1', seats=150, model_number=random_model_number, airline=self.airline)

        with self.assertRaises((IntegrityError, DjangoIntegrityError, ValueError)):
            Airplane.objects.create(
                name='Test Airplane 2', seats=200, model_number=random_model_number, airline=self.airline)

    def test_airplane_str_representation(self):
        random_model_number = self.fake.bothify(text='????####')
        airplane = Airplane.objects.create(name='Test Airplane', seats=100, model_number=random_model_number, airline=self.airline)

        # Check if the __str__ method returns a meaningful representation
        expected_str = f'Airplane {airplane.id} - Name: {airplane.name}, Seats: {airplane.seats}, Model Number: {airplane.model_number}, Airline: {str(airplane.airline)}'
        self.assertEqual(str(airplane), expected_str)




class AirplaneAPITests(APITestCase):
    fixtures = ['airplane/fixtures/initial_data.json']

    def setUp(self):
        self.role = Role.objects.get_or_create(name="authenticated")
        self.user = User.objects.create_user(
            username='testuser', password='testpassword', is_staff=True, role=self.role[0])
        self.client.force_login(self.user)
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token.access_token))

        self.airplane_data = {'name': 'Boeing 757', 'seats': 150, 'model_number': 'BUS W1', 'airline': 1}
        self.second_airplane_data = {'name': 'AWT 7', 'seats': 80, 'model_number': 'A1', 'airline': 2}

    def tearDown(self):
        self.client.logout()

    def test_read_airplane_with_filter(self):
        # create airplane
        self.client.post(reverse('airplane-list'), self.airplane_data, format='json')
        # read airplane
        response_with_pagination = self.client.get(reverse('airplane-list'), {'name__icontains': 'Boeing'}, format='json')

        self.assertEqual(response_with_pagination.status_code, status.HTTP_200_OK)
        response = response_with_pagination.data['results']
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]['name'], 'Boeing 757')

    def test_read_airplane_with_pagination(self):
        # create airplane
        self.client.post(reverse('airplane-list'), self.airplane_data, format='json')
        # read airplane
        response_with_pagination = self.client.get(reverse('airplane-list'), {'name__icontains': 'Boeing'}, format='json')

        self.assertEqual(response_with_pagination.status_code, status.HTTP_200_OK)
        self.assertEqual(response_with_pagination.data['count'], 1)
        self.assertEqual(response_with_pagination.data['next'], None)
        self.assertEqual(response_with_pagination.data['previous'], None)
        response = response_with_pagination.data['results']
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]['name'], 'Boeing 757')

    def test_read_airplane_with_ordering(self):
        # create airplane
        self.client.post(reverse('airplane-list'), self.airplane_data, format='json')
        self.client.post(reverse('airplane-list'), self.second_airplane_data, format='json')
        # read airplane

        # Test reading the airplane with ordering by name
        response_ordered = self.client.get(reverse('airplane-list'), {'ordering': 'name'}, format='json')
        self.assertEqual(response_ordered.status_code, status.HTTP_200_OK)
        self.assertEqual(response_ordered.data['count'], 2)
        self.assertEqual(response_ordered.data['next'], None)
        self.assertEqual(response_ordered.data['previous'], None)

        response = response_ordered.data['results']
        self.assertEqual(response[0]['name'], 'AWT 7')
        self.assertEqual(response[1]['name'], 'Boeing 757')

    def test_update_airplane(self):
        # create airplane
        self.client.post(reverse('airplane-list'), self.airplane_data, format='json')
        # read airplane
        response_filter = self.client.get(
            reverse('airplane-list'), {'name__icontains': 'Boeing'}, format='json')
        airplane = response_filter.data['results'][0]

        # update
        updated_data =  {'name': 'Boeing 787'}
        response = self.client.patch(reverse('airplane-detail', args=[airplane['id']]), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Airplane.objects.get().name, 'Boeing 787')

    def test_delete_airplane(self):
        # create airplane
        self.client.post(reverse('airplane-list'), self.airplane_data, format='json')
        # read airplane
        response_filter = self.client.get(
            reverse('airplane-list'), {'name__icontains': 'Boeing'}, format='json')
        airplane = response_filter.data['results'][0]

        # delete airplane
        response = self.client.delete(reverse('airplane-detail', args=[airplane['id']]), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Airplane.objects.count(), 0)
