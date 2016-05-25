from django.test import TestCase
from django.utils import translation

from apps.core.tests import TestListViewMixin


class QuestionsTestCase(TestCase):
    fixtures = ['accounts/testing.json', 'domain/testing.json', 'questions/testing.json']


class QuestionsTests(TestListViewMixin, QuestionsTestCase):

    list_url_name = 'questions'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
