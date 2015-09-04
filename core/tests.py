import re

from django.test import TestCase, Client
from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.core.urlresolvers import reverse

class ClientTestCase(TestCase):

    def setUp(self):
        User.objects.create_user('test','test@example.com','test')

    def test_home(self):
        """ The home page can be accessed. """

        response = Client().get('/')
        self.assertEqual(response.status_code, 200)

    def test_login_link(self):
        """ The login link is rendered correctly. """

        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.content.find('<a href="%s">Login</a>' % settings.LOGIN_URL), -1)

        c.login(username='test', password='test')
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.content.find('<a href="%s">Logout</a>' % settings.LOGOUT_URL), -1)

    def test_password_change(self):
        """ The user can change his/her password. """

        c = Client()

        # try without being logged in
        response = c.get(reverse('password_change'))
        self.assertEqual(response.status_code, 302)

        # log in
        c.login(username='test', password='test')

        # try again
        response = c.get(reverse('password_change'))
        self.assertEqual(response.status_code, 200)

        # post an invalid form
        response = c.post(reverse('password_change'), {
            'old_password': 'test1',
            'new_password1': 'test1',
            'new_password2': 'test1'
        })
        self.assertEqual(response.status_code, 200)

        # post a valid form
        response = c.post(reverse('password_change'), {
            'old_password': 'test',
            'new_password1': 'test1',
            'new_password2': 'test1'
        })
        self.assertEqual(response.status_code, 302)

    def test_password_reset(self):
        """ The user can rest his/her password if he/she forgot. """

        c = Client()

        # get the password_reset page
        response = c.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)

        # post an ivalid email
        response = c.post(reverse('password_reset'), {
            'email': 'wrong@example.com'
        })
        self.assertRedirects(response, reverse('password_reset_done'))
        self.assertEqual(len(mail.outbox), 0)

        # post a valid email
        response = c.post(reverse('password_reset'), {
            'email': 'test@example.com'
        })
        self.assertRedirects(response, reverse('password_reset_done'))
        self.assertEqual(len(mail.outbox), 1)
