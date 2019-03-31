from django.test import TestCase

from test_generator.viewsets import (
    TestModelViewsetMixin,
    TestListViewsetMixin,
    TestReadOnlyModelViewsetMixin
)

from rdmo.core.testing.mixins import TestTranslationMixin, TestImportViewMixin
from rdmo.accounts.utils import set_group_permissions
from rdmo.options.models import OptionSet
from rdmo.conditions.models import Condition

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
            'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 403
        },
        'detail_viewset': {
            'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 403
        },
        'create_viewset': {
            'editor': 201, 'reviewer': 403, 'api': 403, 'user': 403, 'anonymous': 403
        },
        'update_viewset': {
            'editor': 200, 'reviewer': 403, 'api': 403, 'user': 403, 'anonymous': 403
        },
        'delete_viewset': {
            'editor': 204, 'reviewer': 403, 'api': 403, 'user': 403, 'anonymous': 403
        }
    }

    @classmethod
    def setUpTestData(cls):
        set_group_permissions()


class CatalogTests(TestTranslationMixin, TestModelViewsetMixin, QuestionsViewsetTestCase):

    instances = Catalog.objects.all()
    url_names = {
        'viewset': 'internal-questions:catalog'
    }
    trans_fields = ('title', )

    def _test_create_viewset(self, username):
        for instance in self.instances:
            instance.key += '_new'
            self.assert_create_viewset(username, data=self.get_instance_as_dict(instance))


class SectionTests(TestTranslationMixin, TestModelViewsetMixin, QuestionsViewsetTestCase):

    instances = Section.objects.all()
    url_names = {
        'viewset': 'internal-questions:section'
    }
    trans_fields = ('title', )

    def _test_create_viewset(self, username):
        for instance in self.instances:
            instance.key += '_new'
            self.assert_create_viewset(username, data=self.get_instance_as_dict(instance))


class QuestionSetTests(TestTranslationMixin, TestModelViewsetMixin, QuestionsViewsetTestCase):

    instances = QuestionSet.objects.all()
    url_names = {
        'viewset': 'internal-questions:questionset'
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
        'viewset': 'internal-questions:question'
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


class OptionSetTests(TestReadOnlyModelViewsetMixin, QuestionsViewsetTestCase):

    instances = OptionSet.objects.all()
    url_names = {
        'viewset': 'internal-questions:optionset'
    }


class ConditionTests(TestReadOnlyModelViewsetMixin, QuestionsViewsetTestCase):

    instances = Condition.objects.all()
    url_names = {
        'viewset': 'internal-questions:condition'
    }


class WidgetTypeTests(TestListViewsetMixin, QuestionsViewsetTestCase):

    url_names = {
        'viewset': 'internal-questions:widgettype'
    }
    status_map = {
        'list_viewset': {'editor': 200, 'reviewer': 200, 'api': 200, 'user': 200, 'anonymous': 403}
    }


class CatalogImportTests(TestImportViewMixin, TestCase):

    import_file = 'testing/xml/questions.xml'
    export_api = 'questions_catalog_export'
    export_api_kwargs = {'format': 'xml', 'pk': '1'}


class CatalogAPITests(TestReadOnlyModelViewsetMixin, QuestionsViewsetTestCase):

    instances = Catalog.objects.all()
    url_names = {
        'viewset': 'api-v1-questions:catalog'
    }


class SectionAPITests(TestReadOnlyModelViewsetMixin, QuestionsViewsetTestCase):

    instances = Section.objects.all()
    url_names = {
        'viewset': 'api-v1-questions:section'
    }


class QuestionSetAPITests(TestReadOnlyModelViewsetMixin, QuestionsViewsetTestCase):

    instances = QuestionSet.objects.all()
    url_names = {
        'viewset': 'api-v1-questions:questionset'
    }


class QuestionAPITests(TestReadOnlyModelViewsetMixin, QuestionsViewsetTestCase):

    instances = Question.objects.all()
    url_names = {
        'viewset': 'api-v1-questions:question'
    }
