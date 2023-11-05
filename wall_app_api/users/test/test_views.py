from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from oauth2_provider.models import Application, AccessToken
from ..models import User
import pytz


class UserProfileViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.org', password='_testpassword_')

    def test_user_profile_view_authenticated(self):
        url = reverse('user-profile')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_profile_view_unauthenticated(self):
        url = reverse('user-profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserCreateViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.org', password='_testpassword_')

    def test_user_create_view(self):
        url = reverse('user-create')
        data = {
            'email': 'test1@example.org',
            'password': '_newpassword_',
            'first_name': 'Test',
            'last_name': 'User',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertIn('email', response.data)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)
        self.assertNotIn('password', response.data)
        self.assertNotIn('access_token', response.data)
        self.assertNotIn('refresh_token', response.data)
        self.assertNotIn('token', response.data)
        self.assertEqual(User.objects.count(), 2)

    def test_user_create_view_with_only_mandatory_fields(self):
        url = reverse('user-create')
        data = {
            'email': 'test1@example.org',
            'password': '_newpassword_',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertIn('email', response.data)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)
        self.assertNotIn('password', response.data)
        self.assertNotIn('access_token', response.data)
        self.assertNotIn('refresh_token', response.data)
        self.assertNotIn('token', response.data)
        self.assertEqual(User.objects.count(), 2)

    def test_user_create_view_with_duplicated_email(self):
        url = reverse('user-create')
        data = {
            'email': 'test@example.org',
            'password': '_newpassword_',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_user_create_view_with_invalid_data(self):
        url = reverse('user-create')
        data = {
            'email': 'test1@example.org',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_user_crate_view_with_invalid_password(self):
        url = reverse('user-create')
        data = {
            'email': 'test1@example.org',
            'password': 'password'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
