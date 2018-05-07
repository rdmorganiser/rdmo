from django.test import TestCase

from test_generator.views import TestListViewMixin

from rdmo.core.testing.mixins import TestExportViewMixin, TestImportViewMixin
from rdmo.accounts.utils import set_group_permissions


class ViewsViewTestCase(TestCase):

    fixtures = (
        'users.json',
        'groups.json',
        'accounts.json',
        'conditions.json',
        'domain.json',
        'options.json',
        'views.json',
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
        'import_view': {
            'editor': 302, 'reviewer': 403, 'api': 403, 'user': 403, 'anonymous': 302
        }
    }

    @classmethod
    def setUpTestData(cls):
        set_group_permissions()


class ViewsTests(TestListViewMixin, TestExportViewMixin, TestImportViewMixin, ViewsViewTestCase):

    url_names = {
        'list_view': 'views',
        'export_view': 'views_export',
        'import_view': 'views_import'
    }

    import_file = 'testing/xml/views.xml'
