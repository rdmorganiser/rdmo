from django.test import TestCase

from apps.core.testing.mixins import (
    TestListViewMixin,
    TestExportViewMixin,
    TestImportViewMixin,
    TestModelAPIViewMixin
)

from .models import View


class ViewsTestCase(TestCase):

    lang = 'en'

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
        ('anonymous', None),
    )


class ViewsTests(TestListViewMixin, ViewsTestCase):

    url_names = {
        'list': 'views'
    }
    status_map = {
        'list': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 302}
    }


class ViewTests(TestModelAPIViewMixin, ViewsTestCase):

    instances = View.objects.all()

    api_url_name = 'internal-views:view'
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


class ViewsExportTests(TestExportViewMixin, ViewsTestCase):

    url_names = {
        'export': 'views_export'
    }
    status_map = {
        'export': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 302}
    }


class ViewsImportTests(TestImportViewMixin, TestCase):

    import_file = 'testing/xml/views.xml'
