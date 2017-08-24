from django.test import TestCase

from test_generator.views import TestListViewMixin

from rdmo.core.testing.mixins import TestExportViewMixin, TestImportViewMixin
from rdmo.accounts.utils import set_group_permissions


class DomainViewTestCase(TestCase):

    fixtures = (
        'users.json',
        'groups.json',
        'accounts.json',
        'conditions.json',
        'domain.json',
        'options.json',
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


class DomainTests(TestListViewMixin, DomainViewTestCase):

    url_names = {
        'list_view': 'domain'
    }


class DomainExportTests(TestExportViewMixin, DomainViewTestCase):

    url_names = {
        'list_view': 'domain',
        'export_view': 'domain_export'
    }
    export_formats = ('xml', 'html', 'rtf', 'csv')


class DomainImportTests(TestImportViewMixin, DomainViewTestCase):

    import_file = 'testing/xml/domain.xml'
