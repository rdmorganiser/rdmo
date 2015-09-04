from django.test import TestCase, Client
from django.conf import settings
from django.contrib.auth.models import User

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
