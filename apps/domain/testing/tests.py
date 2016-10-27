from django.test import TestCase
from django.utils import translation

from apps.core.testing.mixins import *
from apps.accounts.testing.factories import AdminFactory
from apps.conditions.testing.factories import ConditionFactory

from .factories import *


class DomainTests(TestListViewMixin, TestCase):

    list_url_name = 'domain'

    def setUp(self):
        translation.activate('en')

        AdminFactory()
        self.client.login(username='admin', password='admin')


class AttributeEntityTests(TestModelAPIViewMixin, TestCase):

    api_url_name = 'domain:entity'

    def setUp(self):
        translation.activate('en')

        AdminFactory()
        self.client.login(username='admin', password='admin')

        self.instance = AttributeEntityFactory()


class AttributeTests(TestModelAPIViewMixin, TestCase):

    api_url_name = 'domain:attribute'

    def setUp(self):
        translation.activate('en')

        AdminFactory()
        self.client.login(username='admin', password='admin')

        self.instance = AttributeFactory()


class RangeTests(TestListAPIViewMixin, TestRetrieveAPIViewMixin, TestUpdateAPIViewMixin, TestDeleteAPIViewMixin, TestCase):

    api_url_name = 'domain:range'

    def setUp(self):
        translation.activate('en')

        AdminFactory()
        self.client.login(username='admin', password='admin')

        self.instance = RangeFactory()


class VerboseNameTests(TestListAPIViewMixin, TestRetrieveAPIViewMixin, TestUpdateAPIViewMixin, TestDeleteAPIViewMixin, TestCase):

    api_url_name = 'domain:verbosename'

    def setUp(self):
        translation.activate('en')

        AdminFactory()
        self.client.login(username='admin', password='admin')

        self.instance = VerboseNameFactory()


class ValueTypeTests(TestListAPIViewMixin, TestCase):

    api_url_name = 'domain:valuestype'

    def setUp(self):
        translation.activate('en')

        AdminFactory()
        self.client.login(username='admin', password='admin')


class OptionSetTests(TestListAPIViewMixin, TestRetrieveAPIViewMixin, TestCase):

    api_url_name = 'domain:optionset'

    def setUp(self):
        translation.activate('en')

        AdminFactory()
        self.client.login(username='admin', password='admin')

        self.instance = OptionSetFactory()


class ConditionTests(TestListAPIViewMixin, TestRetrieveAPIViewMixin, TestCase):

    api_url_name = 'options:condition'

    def setUp(self):
        translation.activate('en')

        AdminFactory()
        self.client.login(username='admin', password='admin')

        self.instance = ConditionFactory()
