from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from role.models import Role
from rest_framework.authtoken.models import Token
from user.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Luggage


class LuggageAPITests(APITestCase):

    def setUp(self):
        self.role = Role.objects.get_or_create(name="authenticated")
        self.user = User.objects.create_user(
            username='testuser', password='testpassword', is_staff=True, role=self.role[0])
        self.client.force_login(self.user)
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token.access_token))

        self.luggage_data = {'name': 'small', 'size': 1, 'unit': 'kg'}
        self.second_luggage_data = {'name': 'large', 'size': 10, 'unit': 'kg'}

    def tearDown(self):
        self.client.logout()

    def test_read_luggage_with_filter(self):
        # create luggage
        self.client.post(reverse('luggage-list'), self.luggage_data, format='json')
        # read luggage
        response_with_pagination = self.client.get(
            reverse('luggage-list'), {'name__icontains': 'small'}, format='json')

        self.assertEqual(response_with_pagination.status_code, status.HTTP_200_OK)
        response = response_with_pagination.data['results']
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]['name'], 'small')

    def test_read_luggage_with_pagination(self):
        # create luggage
        self.client.post(reverse('luggage-list'), self.luggage_data, format='json')
        # read luggage
        response_with_pagination = self.client.get(
            reverse('luggage-list'), {'name__icontains': 'small'}, format='json')

        self.assertEqual(response_with_pagination.status_code, status.HTTP_200_OK)
        self.assertEqual(response_with_pagination.data['count'], 1)
        self.assertEqual(response_with_pagination.data['next'], None)
        self.assertEqual(response_with_pagination.data['previous'], None)
        response = response_with_pagination.data['results']
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]['name'], 'small')

    def test_read_luggage_with_ordering(self):
        # create luggage
        self.client.post(reverse('luggage-list'), self.luggage_data, format='json')
        self.client.post(reverse('luggage-list'), self.second_luggage_data, format='json')
        # read luggage

        # Test reading the luggage with ordering by name
        response_ordered = self.client.get(
            reverse('luggage-list'), {'ordering': 'name'}, format='json')
        self.assertEqual(response_ordered.status_code, status.HTTP_200_OK)
        self.assertEqual(response_ordered.data['count'], 2)
        self.assertEqual(response_ordered.data['next'], None)
        self.assertEqual(response_ordered.data['previous'], None)

        response = response_ordered.data['results']
        self.assertEqual(response[0]['name'], 'large')
        self.assertEqual(response[1]['name'], 'small')

    def test_update_luggage(self):
        # create luggage
        self.client.post(reverse('luggage-list'), self.luggage_data, format='json')
        # read luggage
        response_filter = self.client.get(
            reverse('luggage-list'), {'name__icontains': 'Boeing'}, format='json')
        luggage = response_filter.data['results'][0]

        # update
        updated_data =  {'name': 'Boeing 787'}
        response = self.client.patch(
            reverse('luggage-detail', args=[luggage['id']]), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Luggage.objects.get().name, 'Boeing 787')

    def test_delete_luggage(self):
        # create luggage
        self.client.post(reverse('luggage-list'), self.luggage_data, format='json')
        # read luggage
        response_filter = self.client.get(
            reverse('luggage-list'), {'name__icontains': 'Boeing'}, format='json')
        luggage = response_filter.data['results'][0]

        # delete luggage
        response = self.client.delete(
            reverse('luggage-detail', args=[luggage['id']]), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Luggage.objects.count(), 0)
