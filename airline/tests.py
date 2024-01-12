from django.test import TestCase
from rest_framework.test import APITestCase
from cities_light.models import Country
from role.models import Role
from user.models import User
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
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


class AirlineAPITests(APITestCase):
    fixtures = ['airline/fixtures/initial_data.json']

    def setUp(self):
        self.role = Role.objects.get_or_create(name="authenticated")
        self.user = User.objects.create_user(
            username='testuser', password='testpassword', is_staff=True, role=self.role[0])
        self.client.force_login(self.user)
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token.access_token))

        self.country_turkey = Country.objects.get(code2='TR')
        self.country_st_lucia = Country.objects.get(code2='LC')
        self.airline_data = {'name': 'Turkish Airlines', 'country': self.country_turkey.id}
        self.second_airline_data = {'name': 'Saint Lucia Airlines', 'country': self.country_st_lucia.id}

    def tearDown(self):
        self.client.logout()

    def test_read_airline_with_filter(self):
        # create airline
        self.client.post(reverse('airline-list'), self.airline_data, format='json')
        # read airline
        response_with_pagination = self.client.get(reverse('airline-list'), {'name__icontains': 'Turkish'}, format='json')

        self.assertEqual(response_with_pagination.status_code, status.HTTP_200_OK)
        response = response_with_pagination.data['results']
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]['name'], 'Turkish Airlines')

    def test_read_airline_with_pagination(self):
        # create airline
        self.client.post(reverse('airline-list'), self.airline_data, format='json')
        # read airline
        response_with_pagination = self.client.get(reverse('airline-list'), {'name__icontains': 'Turkish'}, format='json')

        self.assertEqual(response_with_pagination.status_code, status.HTTP_200_OK)
        self.assertEqual(response_with_pagination.data['count'], 1)
        self.assertEqual(response_with_pagination.data['next'], None)
        self.assertEqual(response_with_pagination.data['previous'], None)
        response = response_with_pagination.data['results']
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]['name'], 'Turkish Airlines')

    def test_read_airline_with_ordering(self):
        # create airline
        self.client.post(reverse('airline-list'), self.airline_data, format='json')
        self.client.post(reverse('airline-list'), self.second_airline_data, format='json')
        # read airline

        # Test reading the airline with ordering by name
        response_ordered = self.client.get(reverse('airline-list'), {'ordering': 'name'}, format='json')
        self.assertEqual(response_ordered.status_code, status.HTTP_200_OK)
        self.assertEqual(response_ordered.data['count'], 2)
        self.assertEqual(response_ordered.data['next'], None)
        self.assertEqual(response_ordered.data['previous'], None)

        response = response_ordered.data['results']
        self.assertEqual(response[0]['name'], 'Saint Lucia Airlines')
        self.assertEqual(response[1]['name'], 'Turkish Airlines')

    def test_update_airline(self):
        # create airline
        self.client.post(reverse('airline-list'), self.airline_data, format='json')
        # read airline
        response_filter = self.client.get(
            reverse('airline-list'), {'name__icontains': 'Turkish'}, format='json')
        airline = response_filter.data['results'][0]

        # update
        updated_data =  {'name': 'Turkish Airlines (Nouveau)', 'country': self.country_turkey.id}
        response = self.client.put(reverse('airline-detail', args=[airline['id']]), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Airline.objects.get().name, 'Turkish Airlines (Nouveau)')

    def test_delete_airline(self):
        # create airline
        self.client.post(reverse('airline-list'), self.airline_data, format='json')
        # read airline
        response_filter = self.client.get(
            reverse('airline-list'), {'name__icontains': 'Turkish'}, format='json')
        airline = response_filter.data['results'][0]

        # delete airline
        response = self.client.delete(reverse('airline-detail', args=[airline['id']]), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Airline.objects.count(), 0)
