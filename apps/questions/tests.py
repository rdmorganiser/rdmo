from django.core.urlresolvers import reverse
from django.test import TestCase

from apps.core.testing.mixins import (
    TestListViewMixin,
    TestImportViewMixin,
    TestModelAPIViewMixin,
    TestListAPIViewMixin
)

from .models import Catalog, Section, Subsection, QuestionEntity, Question


class QuestionsTestCase(TestCase):

    lang = 'en'

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
        ('anonymous', None),
    )


class QuestionsTests(TestListViewMixin, QuestionsTestCase):

    url_names = {
        'list': 'catalogs'
    }
    status_map = {
        'list': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 302}
    }


class CatalogTests(TestModelAPIViewMixin, QuestionsTestCase):

    instances = Catalog.objects.all()

    api_url_name = 'internal-questions:catalog'
    api_status_map = {
        'list': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 403},
        'retrieve': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 403},
        'create': {'editor': 201, 'reviewer': 403, 'user': 403, 'anonymous': 403},
        'update': {'editor': 200, 'reviewer': 403, 'user': 403, 'anonymous': 403},
        'delete': {'editor': 204, 'reviewer': 403, 'user': 403, 'anonymous': 403},
        'export': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 302}
    }

    def prepare_create_instance(self, instance):
        instance.key += '_new'
        return instance


class SectionTests(TestModelAPIViewMixin, QuestionsTestCase):

    instances = Section.objects.all()

    api_url_name = 'internal-questions:section'
    api_status_map = {
        'list': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 403},
        'retrieve': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 403},
        'create': {'editor': 201, 'reviewer': 403, 'user': 403, 'anonymous': 403},
        'update': {'editor': 200, 'reviewer': 403, 'user': 403, 'anonymous': 403},
        'delete': {'editor': 204, 'reviewer': 403, 'user': 403, 'anonymous': 403}
    }

    def prepare_create_instance(self, instance):
        instance.key += '_new'
        return instance


class SubsectionTests(TestModelAPIViewMixin, QuestionsTestCase):

    instances = Subsection.objects.all()

    api_url_name = 'internal-questions:subsection'
    api_status_map = {
        'list': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 403},
        'retrieve': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 403},
        'create': {'editor': 201, 'reviewer': 403, 'user': 403, 'anonymous': 403},
        'update': {'editor': 200, 'reviewer': 403, 'user': 403, 'anonymous': 403},
        'delete': {'editor': 204, 'reviewer': 403, 'user': 403, 'anonymous': 403}
    }

    def prepare_create_instance(self, instance):
        instance.key += '_new'
        return instance


class QuestionSetTests(TestModelAPIViewMixin, QuestionsTestCase):

    instances = QuestionEntity.objects.filter(question=None)

    api_url_name = 'internal-questions:questionset'
    api_status_map = {
        'list': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 403},
        'retrieve': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 403},
        'create': {'editor': 201, 'reviewer': 403, 'user': 403, 'anonymous': 403},
        'update': {'editor': 200, 'reviewer': 403, 'user': 403, 'anonymous': 403},
        'delete': {'editor': 204, 'reviewer': 403, 'user': 403, 'anonymous': 403}
    }

    def prepare_create_instance(self, instance):
        instance.key += '_new'
        return instance


class QuestionTests(TestModelAPIViewMixin, QuestionsTestCase):

    instances = Question.objects.all()

    api_url_name = 'internal-questions:question'
    api_status_map = {
        'list': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 403},
        'retrieve': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 403},
        'create': {'editor': 201, 'reviewer': 403, 'user': 403, 'anonymous': 403},
        'update': {'editor': 200, 'reviewer': 403, 'user': 403, 'anonymous': 403},
        'delete': {'editor': 204, 'reviewer': 403, 'user': 403, 'anonymous': 403}
    }

    def prepare_create_instance(self, instance):
        instance.key += '_new'
        return instance


class WidgetTypeTests(TestListAPIViewMixin, QuestionsTestCase):

    api_url_name = 'internal-questions:widgettype'
    api_status_map = {
        'list': {'editor': 200, 'reviewer': 200, 'user': 200, 'anonymous': 200}
    }


class CatalogExportTests(QuestionsTestCase):

    instances = Catalog.objects.all()

    url_names = {
        'export': 'questions_catalog_export'
    }
    status_map = {
        'export': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 302}
    }

    export_formats = ('xml', 'html', 'rtf')

    def test_export_detail(self):

        for username, password in self.users:
            if password:
                self.client.login(username=username, password=password)

            for instance in self.instances:
                for format in self.export_formats:
                    url = reverse(self.url_names['export'], kwargs={
                        'pk': instance.pk,
                        'format': format
                    })
                    response = self.client.get(url)

                    try:
                        self.assertEqual(response.status_code, self.status_map['export'][username])
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
