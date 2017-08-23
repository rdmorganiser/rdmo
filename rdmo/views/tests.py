from django.test import TestCase

from test_generator.views import TestListViewMixin
from test_generator.viewsets import TestModelViewsetMixin, TestListViewsetMixin, TestRetrieveViewsetMixin

from rdmo.core.testing.mixins import TestExportViewMixin, TestImportViewMixin
from rdmo.accounts.utils import set_group_permissions

from .models import View


class ViewsTestCase(TestCase):

    fixtures = (
        'users.json',
        'groups.json',
        'accounts.json',
        'conditions.json',
        'domain.json',
        'options.json',
        'views.json',
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


class ViewsTests(TestListViewMixin, ViewsTestCase):

    url_names = {
        'list_view': 'views'
    }


class ViewTests(TestModelViewsetMixin, ViewsTestCase):

    instances = View.objects.all()
    url_names = {
        'viewset': 'internal-views:view'
    }

    def prepare_create_instance(self, instance):
        instance.key += '_new'
        return instance


class ViewsExportTests(TestExportViewMixin, ViewsTestCase):

    url_names = {
        'export_view': 'views_export'
    }


class ViewsImportTests(TestImportViewMixin, TestCase):

    import_file = 'testing/xml/views.xml'


class ViewAPITests(TestListViewsetMixin, TestRetrieveViewsetMixin, ViewsTestCase):

    instances = View.objects.all()
    url_names = {
        'viewset': 'api-v1-views:view'
    }
