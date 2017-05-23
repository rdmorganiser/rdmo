from django.test import TestCase

from test_mixins.views import TestListViewMixin
from test_mixins.viewsets import TestModelViewsetMixin, TestListViewsetMixin, TestRetrieveViewsetMixin

from apps.core.testing.mixins import TestExportViewMixin, TestImportViewMixin
from apps.accounts.utils import set_group_permissions
from apps.conditions.models import Condition

from .models import Task


class TasksTestCase(TestCase):

    fixtures = (
        'users.json',
        'groups.json',
        'accounts.json',
        'conditions.json',
        'domain.json',
        'options.json',
        'tasks.json',
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


class TasksTests(TestListViewMixin, TasksTestCase):

    url_names = {
        'list_view': 'tasks'
    }


class TaskTests(TestModelViewsetMixin, TasksTestCase):

    instances = Task.objects.all()
    url_names = {
        'viewset': 'internal-tasks:task'
    }

    def prepare_create_instance(self, instance):
        instance.key += '_new'
        return instance


class ConditionTests(TestListViewsetMixin, TestRetrieveViewsetMixin, TasksTestCase):

    instances = Condition.objects.all()
    url_names = {
        'viewset': 'internal-tasks:condition'
    }


class TasksExportTests(TestExportViewMixin, TasksTestCase):

    url_names = {
        'export_view': 'tasks_export'
    }


class TasksImportTests(TestImportViewMixin, TestCase):

    import_file = 'testing/xml/tasks.xml'


class TaskAPITests(TestListViewsetMixin, TestRetrieveViewsetMixin, TasksTestCase):

    instances = Task.objects.all()
    url_names = {
        'viewset': 'api-v1-tasks:task'
    }
