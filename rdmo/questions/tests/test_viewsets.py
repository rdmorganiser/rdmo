from django.test import TestCase

from test_generator.viewsets import TestModelViewsetMixin, TestListViewsetMixin

from rdmo.core.testing.mixins import TestTranslationMixin
from rdmo.accounts.utils import set_group_permissions

from ..models import Catalog, Section, QuestionSet, Question


class QuestionsViewsetTestCase(TestCase):

    fixtures = (
        'users.json',
        'groups.json',
        'accounts.json',
        'conditions.json',
        'domain.json',
        'options.json',
        'questions.json',
    )

    users = (
        ('editor', 'editor'),
        ('reviewer', 'reviewer'),
        ('user', 'user'),
        ('api', 'api'),
        ('anonymous', None),
    )

    status_map = {
        'list_viewset': {
            'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 401
        },
        'detail_viewset': {
            'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 401
        },
        'create_viewset': {
            'editor': 201, 'reviewer': 403, 'api': 201, 'user': 403, 'anonymous': 401
        },
        'update_viewset': {
            'editor': 200, 'reviewer': 403, 'api': 200, 'user': 403, 'anonymous': 401
        },
        'delete_viewset': {
            'editor': 204, 'reviewer': 403, 'api': 204, 'user': 403, 'anonymous': 401
        }
    }

    @classmethod
    def setUpTestData(cls):
        set_group_permissions()


class CatalogTests(TestTranslationMixin, TestModelViewsetMixin, QuestionsViewsetTestCase):

    instances = Catalog.objects.all()
    url_names = {
        'viewset': 'v1-questions:catalog'
    }
    trans_fields = ('title', )

    def _test_create_viewset(self, username):
        for instance in self.instances:
            instance.key += '_new'
            self.assert_create_viewset(username, data=self.get_instance_as_dict(instance))


class SectionTests(TestTranslationMixin, TestModelViewsetMixin, QuestionsViewsetTestCase):

    instances = Section.objects.all()
    url_names = {
        'viewset': 'v1-questions:section'
    }
    trans_fields = ('title', )

    def _test_create_viewset(self, username):
        for instance in self.instances:
            instance.key += '_new'
            self.assert_create_viewset(username, data=self.get_instance_as_dict(instance))


class QuestionSetTests(TestTranslationMixin, TestModelViewsetMixin, QuestionsViewsetTestCase):

    instances = QuestionSet.objects.all()
    url_names = {
        'viewset': 'v1-questions:questionset'
    }
    trans_fields = (
        'title',
        'help',
        'verbose_name',
        'verbose_name_plural',
    )

    def _test_create_viewset(self, username):
        for instance in self.instances:
            instance.key += '_new'
            self.assert_create_viewset(username, data=self.get_instance_as_dict(instance))


class QuestionTests(TestTranslationMixin, TestModelViewsetMixin, QuestionsViewsetTestCase):

    instances = Question.objects.all()
    url_names = {
        'viewset': 'v1-questions:question'
    }
    trans_fields = (
        'text',
        'help',
        'verbose_name',
        'verbose_name_plural',
    )

    def _test_create_viewset(self, username):
        for instance in self.instances:
            instance.key += '_new'
            self.assert_create_viewset(username, data=self.get_instance_as_dict(instance))


class WidgetTypeTests(TestListViewsetMixin, QuestionsViewsetTestCase):

    url_names = {
        'viewset': 'v1-questions:widgettype'
    }
    status_map = {
        'list_viewset': {'editor': 200, 'reviewer': 200, 'api': 200, 'user': 200, 'anonymous': 401}
    }
