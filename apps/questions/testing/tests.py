from django.test import TestCase
from django.utils import translation

from apps.core.testing.mixins import *
from apps.accounts.testing.factories import AdminFactory

from ..models import *
from .factories import *


class QuestionsTests(TestListViewMixin, TestCase):

    list_url_name = 'questions'

    def setUp(self):
        translation.activate('en')

        AdminFactory()
        self.client.login(username='admin', password='admin')


class CatalogTests(TestModelAPIViewMixin, TestCase):

    api_url_name = 'questions:catalog'

    def setUp(self):
        translation.activate('en')

        AdminFactory()
        self.client.login(username='admin', password='admin')

        self.instance = CatalogFactory()


class SectionTests(TestModelAPIViewMixin, TestCase):

    api_url_name = 'questions:section'

    def setUp(self):
        translation.activate('en')

        AdminFactory()
        self.client.login(username='admin', password='admin')

        self.instance = SectionFactory()


class SubsectionTests(TestModelAPIViewMixin, TestCase):

    api_url_name = 'questions:subsection'

    def setUp(self):
        translation.activate('en')

        AdminFactory()
        self.client.login(username='admin', password='admin')

        self.instance = SubsectionFactory()


class QuestionEntityTests(TestListAPIViewMixin, TestRetrieveAPIViewMixin, TestCase):

    api_url_name = 'questions:entity'

    def setUp(self):
        translation.activate('en')

        AdminFactory()
        self.client.login(username='admin', password='admin')

        self.instance = QuestionEntityFactory()


class QuestionTests(TestModelAPIViewMixin, TestCase):

    api_url_name = 'questions:question'

    def setUp(self):
        translation.activate('en')

        AdminFactory()
        self.client.login(username='admin', password='admin')

        self.instance = QuestionFactory()


class WidgetTypeTests(TestListAPIViewMixin, TestCase):

    api_url_name = 'questions:widgettype'

    def setUp(self):
        translation.activate('en')

        AdminFactory()
        self.client.login(username='admin', password='admin')
