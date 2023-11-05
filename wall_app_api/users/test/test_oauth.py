from datetime import datetime, timedelta
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from oauth2_provider.models import Application, AccessToken, RefreshToken
from ..models import User
import pytz


class OAuthTokenTests(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(email='test@example.org', password='_testpassword_')
        self.application = Application.objects.create(
            name='Test Application',
            client_type='password',
            authorization_grant_type='password',
            user=self.test_user,
        )

    def test_token_issuance(self):
        url = '/o/token/'
        data = {
            'grant_type': 'password',
            'username': 'test@example.org',
            'password': '_testpassword_',
            'client_id': self.application.client_id,
        }
        response = self.client.post(url, data, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response_data)
        self.assertIn('refresh_token', response_data)

    def test_invalid_token_request(self):
        url = '/o/token/'
        data = {
            'grant_type': 'password',
            'username': 'test@example.org',
            'password': '_wrongpassword_',
            'client_id': self.application.client_id,
        }
        response = self.client.post(url, data, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('access_token', response_data)
        self.assertNotIn('refresh_token', response_data)

    def test_token_validation(self):
        url = '/o/token/'
        data = {
            'grant_type': 'password',
            'username': 'test@example.org',
            'password': '_testpassword_',
            'client_id': self.application.client_id,
        }
        response = self.client.post(url, data, format='json')
        response_data = response.json()

        access_token = response_data['access_token']

        url = reverse('user-profile')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_expired_token(self):
        url = '/o/token/'
        data = {
            'grant_type': 'password',
            'username': 'test@example.org',
            'password': '_testpassword_',
            'client_id': self.application.client_id,
        }
        response = self.client.post(url, data, format='json')
        response_data = response.json()

        access_token = response_data['access_token']

        AccessToken.objects.filter(token=access_token).update(expires=datetime.now(pytz.utc) - timedelta(minutes=1))

        url = reverse('user-profile')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_client_credentials(self):
        url = '/o/token/'
        data = {
            'grant_type': 'password',
            'username': 'test@example.org',
            'password': '_testpassword_',
            'client_id': 'invalid-client-id',
        }
        response = self.client.post(url, data, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access_token', response_data)
        self.assertNotIn('refresh_token', response_data)


class OAuthTokenRefreshTests(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(email='test@example.org', password='_testpassword_')
        self.token, _ = Token.objects.get_or_create(user=self.test_user)
        self.application = Application.objects.create(
            name='Test Application',
            client_type='password',
            authorization_grant_type='password',
            user=self.test_user,
        )

    def test_token_refresh(self):
        (refreshToken, accessToken) = self.generate_refresh_token()

        url = '/o/token/'
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': str(refreshToken.token),
            'client_id': self.application.client_id,
        }
        response = self.client.post(url, data, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response_data)
        self.assertIn('refresh_token', response_data)
        self.assertNotEqual(accessToken, response_data['access_token'])

    def test_invalid_refresh_token(self):
        url = '/o/token/'
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': 'invalid-refresh-token',
            'client_id': self.application.client_id,
        }
        response = self.client.post(url, data, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('access_token', response_data)
        self.assertNotIn('refresh_token', response_data)

    def test_expired_refresh_token(self):
        (refreshToken, accessToken) = self.generate_refresh_token(True)

        url = '/o/token/'
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': str(refreshToken.token),
            'client_id': self.application.client_id,
        }
        response = self.client.post(url, data, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('access_token', response_data)
        self.assertNotIn('refresh_token', response_data)

    def generate_refresh_token(self, isRevoked=False):
        access_token = AccessToken.objects.create(
            user=self.test_user,
            token=self.token,
            application=self.application,
            expires=datetime.now(pytz.utc) + timedelta(days=1),
        )
        refreshToken = RefreshToken.objects.create(
            user=self.test_user,
            application=self.application,
            token=self.token,
            access_token=access_token,
            revoked=datetime.now(pytz.utc) - timedelta(minutes=1) if isRevoked else None
        )
        return (refreshToken, access_token)
