from django.test import TestCase

from apps.accounts.utils import set_group_permissions
from apps.core.testing.mixins import (
    TestListViewMixin,
    TestExportViewMixin,
    TestImportViewMixin,
    TestModelAPIViewMixin,
    TestListAPIViewMixin,
    TestRetrieveAPIViewMixin
)

from apps.conditions.models import Condition

from .models import Task


class TasksTestCase(TestCase):

    lang = 'en'

    fixtures = (
        'users.json',
        'groups.json',
        'accounts.json',
        'conditions.json',
        'domain.json',
        'options.json',
        'tasks.json',
    )

    users = (
        ('editor', 'editor'),
        ('reviewer', 'reviewer'),
        ('user', 'user'),
        ('api', 'api'),
        ('anonymous', None),
    )

    status_map = {
        'list': {'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 302},
        'export': {'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 302}
    }

    api_status_map = {
        'list': {'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 403},
        'retrieve': {'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 403},
        'create': {'editor': 201, 'reviewer': 403, 'api': 403, 'user': 403, 'anonymous': 403},
        'update': {'editor': 200, 'reviewer': 403, 'api': 403, 'user': 403, 'anonymous': 403},
        'delete': {'editor': 204, 'reviewer': 403, 'api': 403, 'user': 403, 'anonymous': 403}
    }

    def setUp(self):
        set_group_permissions()


class TasksTests(TestListViewMixin, TasksTestCase):

    url_names = {
        'list': 'tasks'
    }


class TaskTests(TestModelAPIViewMixin, TasksTestCase):

    instances = Task.objects.all()

    api_url_name = 'internal-tasks:task'

    def prepare_create_instance(self, instance):
        instance.key += '_new'
        return instance


class ConditionTests(TestListAPIViewMixin, TestRetrieveAPIViewMixin, TasksTestCase):

    instances = Condition.objects.all()

    api_url_name = 'internal-tasks:condition'


class TasksExportTests(TestExportViewMixin, TasksTestCase):

    url_names = {
        'export': 'tasks_export'
    }


class TasksImportTests(TestImportViewMixin, TestCase):

    import_file = 'testing/xml/tasks.xml'


class TaskAPITests(TestListAPIViewMixin, TestRetrieveAPIViewMixin, TasksTestCase):

    instances = Task.objects.all()

    api_url_name = 'api-v1-tasks:task'
