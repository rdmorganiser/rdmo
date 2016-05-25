from django.test import TestCase
from django.utils import translation

from apps.core.tests import TestListViewMixin


class DomainTestCase(TestCase):
    fixtures = ['accounts/testing.json', 'domain/testing.json']


class DomainTests(TestListViewMixin, DomainTestCase):

    list_url_name = 'domain'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
