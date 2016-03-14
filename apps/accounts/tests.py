import re

from django.test import TestCase, Client
from django.core import mail
from django.core.urlresolvers import reverse
from django.utils import translation

from .models import DetailKey, Profile


class ClientTestCase(TestCase):
    fixtures = ['core/testing.json', 'accounts/testing.json']

    def setUp(self):
        translation.activate('en')

    def test_get_profile_update(self):
        """
        An authorized GET request to the profile update form returns the form.
        """
        client = Client()
        client.login(username='user', password='user')

        url = reverse('profile_update')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_profile_update_redirect(self):
        """
        An unauthorized GET request to the profile update form gets
        redirected to login.
        """
        client = Client()

        url = reverse('profile_update')
        response = client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    def test_post_profile_update(self):
        """
        An authorized POST request to the profile update form updates the
        user and redirects to home.
        """
        client = Client()
        client.login(username='user', password='user')

        url = reverse('profile_update')
        response = client.post(url, {
            'email': 'test@example.com',
            'first_name': 'Albert',
            'last_name': 'Admin'
        })
        self.assertRedirects(response, reverse('home'), target_status_code=302)

    def test_post_profile_update_cancel(self):
        """
        An authorized POST request to the profile update form updates with
        cancel redirects to home.
        """
        client = Client()
        client.login(username='user', password='user')

        url = reverse('profile_update')
        response = client.post(url, {
            'email': 'test@example.com',
            'first_name': 'Albert',
            'last_name': 'Admin',
            'cancel': 'cancel'
        })
        self.assertRedirects(response, reverse('home'), target_status_code=302)

    def test_post_profile_update_cancel2(self):
        """
        An authorized POST request to the profile update form updates with
        cancel and the next field redirects to the given url.
        """
        client = Client()
        client.login(username='user', password='user')

        url = reverse('profile_update')
        response = client.post(url, {
            'email': 'test@example.com',
            'first_name': 'Albert',
            'last_name': 'Admin',
            'cancel': 'cancel',
            'next': 'password_change'
        })
        self.assertRedirects(response, reverse('password_change'))

    def test_post_profile_update_next(self):
        """
        An authorized POST request to the profile update form with next field
        updates the user and redirects to the given url.
        """
        client = Client()
        client.login(username='user', password='user')

        url = reverse('profile_update')
        response = client.post(url, {
            'email': 'test@example.com',
            'first_name': 'Albert',
            'last_name': 'Admin',
            'text': 'text',
            'textarea': 'textarea',
            'select': 'a',
            'radio': 'a',
            'multiselect': 'a',
            'checkbox': 'a',
            'next': 'password_change'
        })
        self.assertRedirects(response, reverse('password_change'))

    def test_post_profile_update_next2(self):
        """
        An authorized POST request to the profile update form with next
        field set to profile_update updates the user and redirects to home.
        """
        client = Client()
        client.login(username='user', password='user')

        url = reverse('profile_update')
        response = client.post(url, {
            'email': 'test@example.com',
            'first_name': 'Albert',
            'last_name': 'Admin',
            'text': 'text',
            'textarea': 'textarea',
            'select': 'a',
            'radio': 'a',
            'multiselect': 'a',
            'checkbox': 'a',
            'next': 'profile_update'
        })
        self.assertRedirects(response, reverse('home'), target_status_code=302)

    def test_get_password_change(self):
        """
        An authorized GET request to the password change form returns the form.
        """
        client = Client()
        client.login(username='user', password='user')

        url = reverse('password_change')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_password_change(self):
        """
        An authorized POST request to the password change form updates the
        password and redirects to home.
        """
        client = Client()
        client.login(username='user', password='user')

        url = reverse('password_change')
        response = client.post(url, {
            'old_password': 'user',
            'new_password1': 'resu',
            'new_password2': 'resu',
        })
        self.assertRedirects(response, reverse('password_change_done'))

    def test_get_password_reset(self):
        """
        A GET request to the password reset form returns the form.
        """
        client = Client()

        url = reverse('password_reset')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_password_reset_invalid(self):
        """
        A POST request to the password reset form with an invalid mail address
        sends no mail.
        """
        client = Client()

        url = reverse('password_reset')
        response = client.post(url, {'email': 'wrong@example.com'})
        self.assertRedirects(response, reverse('password_reset_done'))
        self.assertEqual(len(mail.outbox), 0)

    def test_post_password_reset_valid(self):
        """
        A POST request to the password reset form with an invalid mail address
        sends a mail with a correct link.
        """
        client = Client()

        url = reverse('password_reset')
        response = client.post(url, {'email': 'user@example.com'})
        self.assertRedirects(response, reverse('password_reset_done'))
        self.assertEqual(len(mail.outbox), 1)

        # get the link from the mail
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', mail.outbox[0].body)
        self.assertEqual(len(urls), 1)

        # get the password_reset page
        response = client.get(urls[0])
        self.assertEqual(response.status_code, 200)


class ModelTestCase(TestCase):
    fixtures = ['accounts/testing.json']

    def setUp(self):
        translation.activate('en')

    def test_profile_str(self):
        profile = Profile.objects.get(user__username='admin')
        self.assertEqual(profile.user.username, profile.__str__())

    def test_detail_key_str(self):
        detail_key = DetailKey(key='test', label='Test', type='text', required=True)
        self.assertEqual('test', detail_key.__str__())
