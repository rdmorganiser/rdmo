from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import translation

from rdmo.accounts.utils import set_group_permissions


class CoreViewTests(TestCase):

    fixtures = (
        'users.json',
        'groups.json',
        'accounts.json',
    )

    def setUp(self):
        translation.activate('en')
        set_group_permissions()

    def test_home_view(self):
        """ The home page can be accessed. """

        # test as AnonymousUser
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        # test as regular user
        self.client.login(username='user', password='user')
        response = self.client.get('/')
        self.assertRedirects(response, reverse('projects'))

        # test as manager
        self.client.login(username='manager', password='manager')
        response = self.client.get('/')
        self.assertRedirects(response, reverse('projects'))

        # test as admin
        self.client.login(username='admin', password='admin')
        response = self.client.get('/')
        self.assertRedirects(response, reverse('projects'))

    def test_i18n_switcher(self):
        ''' The i18n switcher works. '''

        # get the url to switch to german
        url = reverse('i18n_switcher', args=['de'])

        # switch to german and check if the header is there
        response = self.client.get(url, HTTP_REFERER='http://testserver/')
        self.assertEqual(302, response.status_code)
        self.assertIn('de', response['Content-Language'])

        # get the url to switch to english
        url = reverse('i18n_switcher', args=['en'])

        # switch to german and check if the header is there
        response = self.client.get(url)
        self.assertEqual(302, response.status_code)
        self.assertIn('en', response['Content-Language'])
