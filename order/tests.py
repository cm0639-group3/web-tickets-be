from rest_framework.test import APITestCase
from cities_light.models import City
from role.models import Role
from user.models import User
from flight.models import Flight
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from .models import Order

class OrderAPITests(APITestCase):
    fixtures = ['order/fixtures/initial_data.json']

    def setUp(self):
        self.role = Role.objects.get_or_create(name="authenticated")
        self.user = User.objects.create_user(
            username='testuser', password='testpassword', is_staff=True, role=self.role[0])
        self.client.force_login(self.user)
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token.access_token))

        self.tourist_user = User.objects.get(username='tourist')

        self.flight_bel_arg = Flight.objects.get(name='BEL-ARG')
        self.flight_arg_bel = Flight.objects.get(name='ARG-BEL')
        self.order_data = {'flight': self.flight_bel_arg.id, 'user': self.tourist_user.id}
        self.second_order_data = {'flight': self.flight_arg_bel.id, 'user': self.tourist_user.id}

    def tearDown(self):
        self.client.logout()

    def test_read_order_with_pagination(self):
        # create order
        self.client.post(reverse('order-list'), self.order_data, format='json')
        # read order
        response_with_pagination = self.client.get(reverse('order-list'), {}, format='json')

        self.assertEqual(response_with_pagination.status_code, status.HTTP_200_OK)
        self.assertEqual(response_with_pagination.data['count'], 1)
        self.assertEqual(response_with_pagination.data['next'], None)
        self.assertEqual(response_with_pagination.data['previous'], None)
        response = response_with_pagination.data['results']
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]['flight'], self.flight_bel_arg.id)

    def test_partial_update_order(self):
        # create order
        create_response = self.client.post(reverse('order-list'), self.order_data, format='json')
        # read order
        response_filter = self.client.get(
            reverse('order-list'), {'id': create_response.json()['id']}, format='json')
        order = response_filter.data['results'][0]

        # update
        updated_data =  {'flight': self.flight_arg_bel.id}
        response = self.client.patch(reverse('order-detail', args=[order['id']]), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.get().flight, self.flight_arg_bel)

    def test_delete_order(self):
        # create order
        create_response = self.client.post(reverse('order-list'), self.order_data, format='json')
        # read order
        response_filter = self.client.get(
            reverse('order-list'), {'id': create_response.json()['id']}, format='json')
        order = response_filter.data['results'][0]

        # delete order
        response = self.client.delete(reverse('order-detail', args=[order['id']]), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)
