from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken
)


class AuthViewsTests(TestCase):
    AUTH_URL = 'http://127.0.0.1:8000/api/auth'

    def setUp(self) -> None:
        self.client = APIClient()

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(
            username='test',
            password='testing123',
        )

    @property
    def bearer_token(self):
        """Returns Authorization headers, which can be passed to APIClient instance."""
        refresh = RefreshToken.for_user(self.user)
        return {"HTTP_AUTHORIZATION": f'Bearer {refresh.access_token}'}

    def test_register_user(self):
        url = f'{self.AUTH_URL}/register/'
        data = {
            'username': 'Tester',
            'password': 'tester41',
            'password2': 'tester41',
            'email': 'test@gmail.com',
            'first_name': 'te',
            'last_name': 'st'
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(User.objects.get(username='Tester'))

    def test_get_token(self):
        url = f'{self.AUTH_URL}/login/'
        data = {
            'username': 'test',
            'password': 'testing123',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.json())
        self.assertIn('access', response.json())

    def test_refresh_token(self):
        url = f'{self.AUTH_URL}/login/'
        data = {
            'username': 'test',
            'password': 'testing123',
        }
        result = self.client.post(url, data).json()
        access, refresh = result['access'], result['refresh']
        response = self.client.post(f'{self.AUTH_URL}/login/refresh/', data={
            'refresh': refresh
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('access', result)
        self.assertNotEqual(access, data['access'])

    def test_change_password(self):
        url = f"{self.AUTH_URL}/password/1/"
        data = {
            "password": "testing41",
            "password2": "testing41",
            "old_password": "testing123"
        }
        response = self.client.put(
            url, data, format="json", **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_profile(self):
        url = f"{self.AUTH_URL}/profile/1/"
        data = {
            'username': 'Tester_update',
            'first_name': 'test1',
            'last_name': 'test2',
            'email': 'test@ui.ac.id'
        }
        response = self.client.put(
            url, data, format="json", **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_user(self):
        result = self.client.post(f'{self.AUTH_URL}/login/', data={
            'username': 'test',
            'password': 'testing123',
        }).json()

        access, refresh = result['access'], result['refresh']
        url = f'{self.AUTH_URL}/logout/'
        data = {
            "refresh": refresh
        }
        response = self.client.post(
            url, data, format="json", **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_outstanding_and_blacklist_token(self):
        result = self.client.post(f'{self.AUTH_URL}/login/', data={
            'username': 'test',
            'password': 'testing123',
        }).json()
        self.assertEqual(OutstandingToken.objects.count(), 1)
        access, refresh = result['access'], result['refresh']
        url = f'{self.AUTH_URL}/logout/'
        data = {
            "refresh": refresh
        }
        response = self.client.post(
            url, data, format="json", **self.bearer_token)
        self.assertEqual(BlacklistedToken.objects.count(), 1)
