from django.test import TestCase
from django.utils import translation

from apps.core.testing.mixins import *
from apps.accounts.testing.factories import AdminFactory
from apps.conditions.testing.factories import ConditionFactory

from .factories import *


class TasksTests(TestListViewMixin, TestCase):

    list_url_name = 'tasks'

    def setUp(self):
        translation.activate('en')

        AdminFactory()
        self.client.login(username='admin', password='admin')


class TaskTests(TestModelAPIViewMixin, TestCase):

    api_url_name = 'tasks:task'

    def setUp(self):
        translation.activate('en')

        AdminFactory()
        self.client.login(username='admin', password='admin')

        self.instance = TaskFactory()


class ConditionTests(TestListAPIViewMixin, TestRetrieveAPIViewMixin, TestCase):

    api_url_name = 'options:condition'

    def setUp(self):
        translation.activate('en')

        AdminFactory()
        self.client.login(username='admin', password='admin')

        self.instance = ConditionFactory()
