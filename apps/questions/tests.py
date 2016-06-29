from django.test import TestCase
from django.utils import translation

from apps.core.test_mixins import *

from .models import *


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


class CatalogTests(TestModelAPIViewMixin, QuestionsTestCase):

    api_url_name = 'questions:catalog'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instance = Catalog.objects.first()


class SectionTests(TestModelAPIViewMixin, QuestionsTestCase):

    api_url_name = 'questions:section'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instance = Section.objects.first()


class SubsectionTests(TestModelAPIViewMixin, QuestionsTestCase):

    api_url_name = 'questions:subsection'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instance = Subsection.objects.first()


class QuestionEntityTests(TestListAPIViewMixin, TestRetrieveAPIViewMixin, QuestionsTestCase):

    api_url_name = 'questions:entity'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instance = QuestionEntity.objects.first()


class QuestionTests(TestModelAPIViewMixin, QuestionsTestCase):

    api_url_name = 'questions:question'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instance = Question.objects.first()


class WidgetTypeTests(TestListAPIViewMixin, QuestionsTestCase):

    api_url_name = 'questions:widgettype'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
