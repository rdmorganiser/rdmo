from django.test import TestCase
from django.utils import translation

from apps.core.testing.mixins import *
from apps.accounts.testing.factories import AdminFactory
from apps.conditions.testing.factories import ConditionFactory

from .factories import *


class OptionsTests(TestListViewMixin, TestCase):

    list_url_name = 'options'

    def setUp(self):
        translation.activate('en')

        AdminFactory()
        self.client.login(username='admin', password='admin')


class OptionSetTests(TestModelAPIViewMixin, TestCase):

    api_url_name = 'options:optionset'

    def setUp(self):
        translation.activate('en')

        AdminFactory()
        self.client.login(username='admin', password='admin')

        self.instance = OptionSetFactory()


class OptionTests(TestModelAPIViewMixin, TestCase):

    api_url_name = 'options:option'

    def setUp(self):
        translation.activate('en')

        AdminFactory()
        self.client.login(username='admin', password='admin')

        self.instance = OptionFactory()


class ConditionTests(TestListAPIViewMixin, TestRetrieveAPIViewMixin, TestCase):

    api_url_name = 'options:condition'

    def setUp(self):
        translation.activate('en')

        AdminFactory()
        self.client.login(username='admin', password='admin')

        self.instance = ConditionFactory()
