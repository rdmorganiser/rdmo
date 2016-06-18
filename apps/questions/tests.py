from django.test import TestCase
from django.utils import translation

from apps.core.test_mixins import *


class QuestionsTestCase(TestCase):
    fixtures = [
        'testing/accounts.json',
        'testing/domain.json',
        'testing/questions.json'
    ]


class QuestionsTests(TestListViewMixin, QuestionsTestCase):

    list_url_name = 'questions'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
