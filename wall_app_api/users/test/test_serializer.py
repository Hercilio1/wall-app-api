from django.test import TestCase
from django.forms.models import model_to_dict
from django.contrib.auth.hashers import check_password
from ..serializers import CreateUserSerializer
from ..models import User

class TestCreateUserSerializer(TestCase):

    def test_serializer(self):
        user_data = User.objects.create_user(email='test@example.org', password='_testpassword_')
        serializer = CreateUserSerializer(user_data)
        expectedData = {
            'id': str(user_data.id),
            'email': user_data.email,
            'first_name': user_data.first_name,
            'last_name': user_data.last_name,
        }
        self.assertEqual(expectedData, serializer.data)

    def test_valid_password(self):
        serializer = CreateUserSerializer(data={
            'email': 'test@example.org',
            'password': '_testpassword_'
        })
        self.assertTrue(serializer.is_valid())

    def test_weak_password(self):
        serializer = CreateUserSerializer(data={
            'email': 'test@example.org',
            'password': 'password'
        })
        self.assertFalse(serializer.is_valid())

    def test_short_password(self):
        serializer = CreateUserSerializer(data={
            'email': 'test@example.org',
            'password': 'pass'
        })
        self.assertFalse(serializer.is_valid())


