from django.test import TestCase, Client

class ClientTestCase(TestCase):

    def setUp(self):
        pass

    def test_home(self):
        """ The home page can be accessed """
        response = Client().get('/')
        self.assertEqual(response.status_code, 200)
