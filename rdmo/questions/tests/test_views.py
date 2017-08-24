from django.core.urlresolvers import reverse
from django.test import TestCase

from test_generator.views import TestListViewMixin

from rdmo.core.testing.mixins import TestImportViewMixin
from rdmo.accounts.utils import set_group_permissions

from ..models import Catalog


class QuestionsViewTestCase(TestCase):

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
        'list_view': {
            'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 302
        },
        'export_view': {
            'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 302
        }
    }

    @classmethod
    def setUpTestData(cls):
        set_group_permissions()


class QuestionsTests(TestListViewMixin, QuestionsViewTestCase):

    url_names = {
        'list_view': 'catalogs'
    }


class CatalogExportTests(QuestionsViewTestCase):

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


class CatalogImportTests(TestImportViewMixin, QuestionsViewTestCase):

    import_file = 'testing/xml/catalog.xml'
