from django.test import TestCase

from apps.core.testing.mixins import (
    TestListViewMixin,
    TestExportListViewMixin,
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
        ('anonymous', None),
    )


class TasksTests(TestListViewMixin, TestExportListViewMixin, TasksTestCase):

    url_names = {
        'list': 'tasks',
        'export': 'tasks_export'
    }
    status_map = {
        'list': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 302},
        'export': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 302}
    }


class TaskTests(TestModelAPIViewMixin, TasksTestCase):

    instances = Task.objects.all()

    api_url_name = 'tasks:task'
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


class ConditionTests(TestListAPIViewMixin, TestRetrieveAPIViewMixin, TasksTestCase):

    instances = Condition.objects.all()

    api_url_name = 'tasks:condition'
    api_status_map = {
        'list': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 403},
        'retrieve': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 403}
    }
