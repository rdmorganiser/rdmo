from django.test import TestCase
from django.utils import translation

from apps.core.testing.mixins import (
    TestListViewMixin,
    TestModelAPIViewMixin,
    TestListAPIViewMixin
)

from .models import Catalog, Section, Subsection, QuestionEntity, Question


class QuestionsTestCase(TestCase):

    fixtures = (
        'users.json',
        'groups.json',
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

    def prepare_create_instance(self, instance):
        instance.key += '_new'
        return instance


class SectionTests(TestModelAPIViewMixin, QuestionsTestCase):

    api_url_name = 'questions:section'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instances = Section.objects.all()

    def prepare_create_instance(self, instance):
        instance.key += '_new'
        return instance


class SubsectionTests(TestModelAPIViewMixin, QuestionsTestCase):

    api_url_name = 'questions:subsection'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instances = Subsection.objects.all()

    def prepare_create_instance(self, instance):
        instance.key += '_new'
        return instance


class QuestionSetTests(TestModelAPIViewMixin, QuestionsTestCase):

    api_url_name = 'questions:questionset'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instances = QuestionEntity.objects.filter(question=None)

    def prepare_create_instance(self, instance):
        instance.key += '_new'
        return instance


class QuestionTests(TestModelAPIViewMixin, QuestionsTestCase):

    api_url_name = 'questions:question'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instances = Question.objects.all()

    def prepare_create_instance(self, instance):
        instance.key += '_new'
        return instance


class WidgetTypeTests(TestListAPIViewMixin, QuestionsTestCase):

    api_url_name = 'questions:widgettype'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
