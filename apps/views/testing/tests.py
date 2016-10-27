from django.test import TestCase
from django.utils import translation

from apps.core.testing.mixins import *
from apps.accounts.testing.factories import AdminFactory

from .factories import *


class TasksTests(TestListViewMixin, TestCase):

    list_url_name = 'views'

    def setUp(self):
        translation.activate('en')

        AdminFactory()
        self.client.login(username='admin', password='admin')


class TaskTests(TestModelAPIViewMixin, TestCase):

    api_url_name = 'views:view'

    def setUp(self):
        translation.activate('en')

        AdminFactory()
        self.client.login(username='admin', password='admin')

        self.instance = ViewFactory()
