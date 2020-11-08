from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from users.models import Address
from users.serializers import AddressSerializer

ADDRESS_URL = reverse('address')


def sample_address(user, **params):
    defaults = {
        'city': 'Moscow',
        'street': 'test'
    }
    defaults.update(**params)

    return Address.objects.create(user=user, **defaults)


class PublicAddressApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(ADDRESS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAddressApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@test.ru',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_address(self):
        sample_address(user=self.user)
        sample_address(user=self.user)
        res = self.client.get(ADDRESS_URL)

        addresses = Address.objects.all()
        serializer = AddressSerializer(addresses, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def addresses_limited_to_user(self):
        user2 = get_user_model().objects.create_user(
            'test2@test.ru',
            'testpass'
        )
        sample_address(user=user2)
        sample_address(user=self.user)
        res = self.client.get(ADDRESS_URL)

        addresses = Address.objects.filter(user=self.user)
        serializer = AddressSerializer(addresses, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)




