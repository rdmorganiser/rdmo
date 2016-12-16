from django.test import TestCase
from django.utils import translation

from apps.core.testing.mixins import *

from .models import *


class QuestionsTestCase(TestCase):

    fixtures = (
        'auth.json',
        'accounts.json',
        'conditions.json',
        'domain.json',
        'options.json',
        'questions.json',
    )


class QuestionsTests(TestListViewMixin, QuestionsTestCase):

    list_url_name = 'catalogs'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')


class CatalogTests(TestModelAPIViewMixin, QuestionsTestCase):

    api_url_name = 'questions:catalog'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instances = Catalog.objects.all()


class SectionTests(TestModelAPIViewMixin, QuestionsTestCase):

    api_url_name = 'questions:section'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')

        self.instances = Section.objects.all()


class SubsectionTests(TestModelAPIViewMixin, QuestionsTestCase):

    api_url_name = 'questions:subsection'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')

        self.instances = Subsection.objects.all()


class QuestionSetTests(TestModelAPIViewMixin, QuestionsTestCase):

    api_url_name = 'questions:questionset'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')

        self.instances = QuestionEntity.objects.filter(question=None)


class QuestionTests(TestModelAPIViewMixin, QuestionsTestCase):

    api_url_name = 'questions:question'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')

        self.instances = Question.objects.all()


class WidgetTypeTests(TestListAPIViewMixin, QuestionsTestCase):

    api_url_name = 'questions:widgettype'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
