from django.test import TestCase
from django.utils import translation

from apps.core.testing.mixins import *

from apps.conditions.models import Condition

from .models import *


class TasksTestCase(TestCase):

    fixtures = (
        'auth.json',
        'accounts.json',
        'conditions.json',
        'domain.json',
        'options.json',
        'tasks.json',
    )


class TasksTests(TestListViewMixin, TasksTestCase):

    list_url_name = 'tasks'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')


class TaskTests(TestModelAPIViewMixin, TasksTestCase):

    api_url_name = 'tasks:task'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instances = Task.objects.all()

    def prepare_create_instance(self, instance):
        instance.identifier += '_new'
        return instance


class ConditionTests(TestListAPIViewMixin, TestRetrieveAPIViewMixin, TasksTestCase):

    api_url_name = 'tasks:condition'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instances = Condition.objects.all()
