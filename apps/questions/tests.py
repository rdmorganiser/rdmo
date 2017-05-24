from django.core.urlresolvers import reverse
from django.test import TestCase

from test_generator.views import TestListViewMixin
from test_generator.viewsets import TestModelViewsetMixin, TestListViewsetMixin, TestRetrieveViewsetMixin

from apps.core.testing.mixins import TestImportViewMixin
from apps.accounts.utils import set_group_permissions

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

    languages = (
        'en',
    )

    users = (
        ('editor', 'editor'),
        ('reviewer', 'reviewer'),
        ('user', 'user'),
        ('api', 'api'),
        ('anonymous', None),
    )

    status_map = {
        'list_view': {
            'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 302
        },
        'export_view': {
            'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 302
        },
        'list_viewset': {
            'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 403
        },
        'retrieve_viewset': {
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


class QuestionsTests(TestListViewMixin, QuestionsTestCase):

    url_names = {
        'list_view': 'catalogs'
    }


class CatalogTests(TestModelViewsetMixin, QuestionsTestCase):

    instances = Catalog.objects.all()
    url_names = {
        'viewset': 'internal-questions:catalog'
    }

    def prepare_create_instance(self, instance):
        instance.key += '_new'
        return instance


class SectionTests(TestModelViewsetMixin, QuestionsTestCase):

    instances = Section.objects.all()
    url_names = {
        'viewset': 'internal-questions:section'
    }

    def prepare_create_instance(self, instance):
        instance.key += '_new'
        return instance


class SubsectionTests(TestModelViewsetMixin, QuestionsTestCase):

    instances = Subsection.objects.all()
    url_names = {
        'viewset': 'internal-questions:subsection'
    }

    def prepare_create_instance(self, instance):
        instance.key += '_new'
        return instance


class QuestionSetTests(TestModelViewsetMixin, QuestionsTestCase):

    instances = QuestionEntity.objects.filter(question=None)
    url_names = {
        'viewset': 'internal-questions:questionset'
    }

    def prepare_create_instance(self, instance):
        instance.key += '_new'
        return instance


class QuestionTests(TestModelViewsetMixin, QuestionsTestCase):

    instances = Question.objects.all()
    url_names = {
        'viewset': 'internal-questions:question'
    }

    def prepare_create_instance(self, instance):
        instance.key += '_new'
        return instance


class WidgetTypeTests(TestListViewsetMixin, QuestionsTestCase):

    url_names = {
        'viewset': 'internal-questions:widgettype'
    }
    status_map = {
        'list_viewset': {'editor': 200, 'reviewer': 200, 'api': 200, 'user': 200, 'anonymous': 403}
    }


class CatalogExportTests(QuestionsTestCase):

    instances = Catalog.objects.all()
    url_names = {
        'export_view': 'questions_catalog_export'
    }
    export_formats = ('xml', 'html', 'rtf')

    def _test_export_detail(self, username, password):

        if password:
            self.client.login(username=username, password=password)

        for instance in self.instances:
            for format in self.export_formats:
                url = reverse(self.url_names['export_view'], kwargs={
                    'pk': instance.pk,
                    'format': format
                })
                response = self.client.get(url)

                try:
                    self.assertEqual(response.status_code, self.status_map['export_view'][username])
                except AssertionError:
                    print(
                        ('test', 'test_export'),
                        ('username', username),
                        ('url', url),
                        ('format', format),
                        ('status_code', response.status_code),
                        ('content', response.content)
                    )
                    raise

        self.client.logout()


class CatalogImportTests(TestImportViewMixin, TestCase):

    import_file = 'testing/xml/catalog.xml'


class CatalogAPITests(TestListViewsetMixin, TestRetrieveViewsetMixin, QuestionsTestCase):

    instances = Catalog.objects.all()
    url_names = {
        'viewset': 'api-v1-questions:catalog'
    }


class SectionAPITests(TestListViewsetMixin, TestRetrieveViewsetMixin, QuestionsTestCase):

    instances = Section.objects.all()
    url_names = {
        'viewset': 'api-v1-questions:section'
    }


class SubsectionAPITests(TestListViewsetMixin, TestRetrieveViewsetMixin, QuestionsTestCase):

    instances = Subsection.objects.all()
    url_names = {
        'viewset': 'api-v1-questions:subsection'
    }


class QuestionSetAPITests(TestListViewsetMixin, TestRetrieveViewsetMixin, QuestionsTestCase):

    instances = QuestionEntity.objects.filter(question=None)
    url_names = {
        'viewset': 'api-v1-questions:questionset'
    }


class QuestionAPITests(TestListViewsetMixin, TestRetrieveViewsetMixin, QuestionsTestCase):

    instances = Question.objects.all()
    url_names = {
        'viewset': 'api-v1-questions:question'
    }
