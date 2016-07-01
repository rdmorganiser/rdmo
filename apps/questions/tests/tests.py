from django.test import TestCase
from django.utils import translation

from apps.core.test_mixins import *

from ..models import *
from .factories import *


class QuestionsTestCase(TestCase):
    fixtures = [
        'testing/accounts.json'
    ]


class QuestionsTests(TestListViewMixin, QuestionsTestCase):

    list_url_name = 'questions'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')


class CatalogTests(TestModelAPIViewMixin, QuestionsTestCase):

    api_url_name = 'questions:catalog'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instance = CatalogFactory()


class SectionTests(TestModelAPIViewMixin, QuestionsTestCase):

    api_url_name = 'questions:section'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instance = SectionFactory()


class SubsectionTests(TestModelAPIViewMixin, QuestionsTestCase):

    api_url_name = 'questions:subsection'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instance = SubsectionFactory()


class QuestionEntityTests(TestListAPIViewMixin, TestRetrieveAPIViewMixin, QuestionsTestCase):

    api_url_name = 'questions:entity'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instance = QuestionEntityFactory()


class QuestionTests(TestModelAPIViewMixin, QuestionsTestCase):

    api_url_name = 'questions:question'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instance = QuestionFactory()


class WidgetTypeTests(TestListAPIViewMixin, QuestionsTestCase):

    api_url_name = 'questions:widgettype'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
