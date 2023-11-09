from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from wall_app_api.users.models import User
from ..models import Entry


class EntryTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.org', password='_testpassword_')

    #
    # CREATE TESTS
    #

    def test_create_entry(self):
        url = reverse('entry-create')
        data = {'content': 'Sample Content'}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Entry.objects.count(), 1)
        entry = Entry.objects.get()
        self.assertEqual(entry.content, 'Sample Content')
        self.assertEqual(entry.user, self.user)

    def test_create_entry_without_logged_in_user(self):
        url = reverse('entry-create')
        data = {'content': 'Sample Content'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_entry_without_content(self):
        url = reverse('entry-create')
        data = {}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_entry_with_empty_content(self):
        url = reverse('entry-create')
        data = {'content': ''}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_entry_with_content_over_280_chars(self):
        url = reverse('entry-create')
        data = {'content': 'a' * 281}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    #
    # READ TESTS
    #

    def test_get_entry_list(self):
        url = reverse('entry-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_entry_detail(self):
        entry = Entry.objects.create(content='Sample Content', user=self.user)
        url = reverse('entry-detail', kwargs={'pk': entry.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_entry_detail_without_logged_in_user(self):
        """
        The user must be authenticated to view an individual entry's details.
        """
        entry = Entry.objects.create(content='Sample Content', user=self.user)
        url = reverse('entry-detail', kwargs={'pk': entry.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_entry_detail_with_diff_user(self):
        """
        Even though it is a different user, the user is authenticated and is using a safe method (GET).
        """
        entry = Entry.objects.create(content='Sample Content', user=self.user)
        url = reverse('entry-detail', kwargs={'pk': entry.pk})
        diff_user = User.objects.create_user(email='test.diff.user@example.org', password='_testpassword_')
        self.client.force_authenticate(user=diff_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #
    # UPDATE TESTS
    #

    def test_update_entry(self):
        entry = Entry.objects.create(content='Sample Content', user=self.user)
        url = reverse('entry-detail', kwargs={'pk': entry.pk})
        data = {'content': 'Updated Content'}
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        entry.refresh_from_db()
        self.assertEqual(entry.content, 'Updated Content')

    def test_update_entry_without_logged_in_user(self):
        entry = Entry.objects.create(content='Sample Content', user=self.user)
        url = reverse('entry-detail', kwargs={'pk': entry.pk})
        data = {'content': 'Updated Content'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(entry.content, 'Sample Content')

    def test_update_entry_with_diff_user(self):
        entry = Entry.objects.create(content='Sample Content', user=self.user)
        url = reverse('entry-detail', kwargs={'pk': entry.pk})
        data = {'content': 'Updated Content'}
        diff_user = User.objects.create_user(email='test.diff.user@example.org', password='_testpassword_')
        self.client.force_authenticate(user=diff_user)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(entry.content, 'Sample Content')

    #
    # DELETE TESTS
    #

    def test_delete_entry(self):
        entry = Entry.objects.create(content='Sample Content', user=self.user)
        url = reverse('entry-detail', kwargs={'pk': entry.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Entry.objects.count(), 0)

    def test_delete_entry_without_logged_in_user(self):
        entry = Entry.objects.create(content='Sample Content', user=self.user)
        url = reverse('entry-detail', kwargs={'pk': entry.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Entry.objects.count(), 1)

    def test_delete_entry_with_diff_user(self):
        entry = Entry.objects.create(content='Sample Content', user=self.user)
        url = reverse('entry-detail', kwargs={'pk': entry.pk})
        diff_user = User.objects.create_user(email='test.diff.user@example.org', password='_testpassword_')
        self.client.force_authenticate(user=diff_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Entry.objects.count(), 1)
