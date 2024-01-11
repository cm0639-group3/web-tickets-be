from rest_framework.test import APITestCase
from cities_light.models import City
from role.models import Role
from user.models import User
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from .models import Airport

class AirportAPITests(APITestCase):
    fixtures = ['airport/fixtures/initial_data.json']

    def setUp(self):
        self.role = Role.objects.get_or_create(name="authenticated")
        self.user = User.objects.create_user(
            username='testuser', password='testpassword', is_staff=True, role=self.role[0])
        self.client.force_login(self.user)
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token.access_token))

        self.city_pontevedra = City.objects.get(slug='pontevedra')
        self.city_sint_andries = City.objects.get(slug='sint-andries')
        self.airport_data = {'name': 'Pontevedra Airport', 'city': self.city_pontevedra.id, 'code': 'AR5'}
        self.second_airport_data = {'name': 'Sint-Andries Flughafen', 'city': self.city_sint_andries.id, 'code': 'BE1'}

    def tearDown(self):
        self.client.logout()

    def test_read_airport_with_filter(self):
        # create airport
        self.client.post(reverse('airport-list'), self.airport_data, format='json')
        # read airport
        response_with_pagination = self.client.get(reverse('airport-list'), {'name__icontains': 'Ponte'}, format='json')

        self.assertEqual(response_with_pagination.status_code, status.HTTP_200_OK)
        response = response_with_pagination.data['results']
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]['name'], 'Pontevedra Airport')

    def test_read_airport_with_pagination(self):
        # create airport
        self.client.post(reverse('airport-list'), self.airport_data, format='json')
        # read airport
        response_with_pagination = self.client.get(reverse('airport-list'), {'name__icontains': 'Ponte'}, format='json')

        self.assertEqual(response_with_pagination.status_code, status.HTTP_200_OK)
        self.assertEqual(response_with_pagination.data['count'], 1)
        self.assertEqual(response_with_pagination.data['next'], None)
        self.assertEqual(response_with_pagination.data['previous'], None)
        response = response_with_pagination.data['results']
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]['name'], 'Pontevedra Airport')

    def test_read_airport_with_ordering(self):
        # create airport
        self.client.post(reverse('airport-list'), self.airport_data, format='json')
        self.client.post(reverse('airport-list'), self.second_airport_data, format='json')
        # read airport

        # Test reading the airport with ordering by name
        response_ordered = self.client.get(reverse('airport-list'), {'ordering': 'name'}, format='json')
        self.assertEqual(response_ordered.status_code, status.HTTP_200_OK)
        self.assertEqual(response_ordered.data['count'], 2)
        self.assertEqual(response_ordered.data['next'], None)
        self.assertEqual(response_ordered.data['previous'], None)

        response = response_ordered.data['results']
        self.assertEqual(response[0]['name'], 'Pontevedra Airport')
        self.assertEqual(response[1]['name'], 'Sint-Andries Flughafen')

    def test_partial_update_airport(self):
        # create airport
        self.client.post(reverse('airport-list'), self.airport_data, format='json')
        # read airport
        response_filter = self.client.get(
            reverse('airport-list'), {'name__icontains': 'Ponte'}, format='json')
        airport = response_filter.data['results'][0]

        # update
        updated_data =  {'name': 'Pontevedra Airport (Ext)'}
        response = self.client.patch(reverse('airport-detail', args=[airport['id']]), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Airport.objects.get().name, 'Pontevedra Airport (Ext)')

    def test_delete_airport(self):
        # create airport
        self.client.post(reverse('airport-list'), self.airport_data, format='json')
        # read airport
        response_filter = self.client.get(
            reverse('airport-list'), {'name__icontains': 'Ponte'}, format='json')
        airport = response_filter.data['results'][0]

        # delete airport
        response = self.client.delete(reverse('airport-detail', args=[airport['id']]), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Airport.objects.count(), 0)
