from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from .models import DetailKey, Profile


class ClientTestCase(TestCase):

    def setUp(self):
        DetailKey.objects.create(key='text', label='Text', type='text', required=True)
        DetailKey.objects.create(key='select', label='Select', type='select', options={'a': 'A', 'b': 'B'}, required=False)
        DetailKey.objects.create(key='radio', label='radio', type='radio', options={'a': 'A', 'b': 'B'}, required=False)
        DetailKey.objects.create(key='multiselect', label='multiselect', type='multiselect', options={'a': 'A', 'b': 'B'}, required=False)
        DetailKey.objects.create(key='checkbox', label='checkbox', type='checkbox', options={'a': 'A', 'b': 'B'}, required=False)

        user = User.objects.create_user('test', 'test@example.com', 'test')
        user.profile.save()

    def test_profile_update(self):
        """ The user profile can be updated. """

        # get the url of the home page
        url = reverse('profile_update')

        # get the client object
        client = Client()

        # try to get the form and get a redirect to the login page
        response = client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

        # login
        client.login(username='test', password='test')

        # try to get the form again
        response = client.get(url)
        self.assertEqual(200, response.status_code)

        # try to post to the form
        response = client.post(url, {
            'username': 'test2',
            'email': 'test2@example.com',
            'first_name': 'Tanja',
            'last_name': 'Test',
            'text': 'test2'
        })
        self.assertRedirects(response, reverse('home'))

        # try to post to the form with a next field
        response = client.post(url, {
            'username': 'test2',
            'email': 'test2@example.com',
            'first_name': 'Tanja',
            'last_name': 'Test',
            'text': 'test2',
            'next': 'http://testserver' + reverse('password_change')
        })
        self.assertRedirects(response, reverse('password_change'))

        # try to post to the form with a next field set to the profile_update url itself
        response = client.post(url, {
            'username': 'test2',
            'email': 'test2@example.com',
            'first_name': 'Tanja',
            'last_name': 'Test',
            'text': 'test2',
            'next': 'http://testserver' + url
        })
        self.assertRedirects(response, reverse('home'))


class ModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('test', 'test@example.com', 'test')

    def test_profile_str(self):
        profile = Profile(user=self.user)
        self.assertEqual(self.user.username, profile.__str__())

    def test_detail_key_str(self):
        detail_key = DetailKey(key='test', label='Test', type='text', required=True)
        self.assertEqual('test', detail_key.__str__())
