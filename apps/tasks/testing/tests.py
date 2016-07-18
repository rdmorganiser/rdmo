from django.test import TestCase
from django.utils import translation

from apps.core.testing.mixins import *
from apps.accounts.testing.factories import AdminFactory

from .factories import *


class TaskTests(TestModelAPIViewMixin, TestCase):

    api_url_name = 'tasks:task'

    def setUp(self):
        translation.activate('en')

        AdminFactory()
        self.client.login(username='admin', password='admin')

        self.instance = TaskFactory()
