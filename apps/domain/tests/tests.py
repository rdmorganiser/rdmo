from django.test import TestCase
from django.utils import translation

from apps.core.test_mixins import *

from .factories import *


class DomainTestCase(TestCase):
    fixtures = [
        'testing/accounts.json'
    ]


class DomainTests(TestListViewMixin, DomainTestCase):

    list_url_name = 'domain'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')


class AttributeEntityTests(TestModelAPIViewMixin, DomainTestCase):

    api_url_name = 'domain:entity'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instance = AttributeEntityFactory()


class AttributeTests(TestModelAPIViewMixin, DomainTestCase):

    api_url_name = 'domain:attribute'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instance = AttributeFactory()


class OptionTests(TestModelAPIViewMixin, DomainTestCase):

    api_url_name = 'domain:option'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instance = OptionFactory()


class RangeTests(TestListAPIViewMixin, TestRetrieveAPIViewMixin, TestUpdateAPIViewMixin, TestDeleteAPIViewMixin, DomainTestCase):

    api_url_name = 'domain:range'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instance = RangeFactory()


class ConditionTests(TestModelAPIViewMixin, DomainTestCase):

    api_url_name = 'domain:condition'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instance = ConditionFactory()


class VerboseNameTests(TestListAPIViewMixin, TestRetrieveAPIViewMixin, TestUpdateAPIViewMixin, TestDeleteAPIViewMixin, DomainTestCase):

    api_url_name = 'domain:verbosename'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instance = VerboseNameFactory()


class ValueTypeTests(TestListAPIViewMixin, DomainTestCase):

    api_url_name = 'domain:valuestype'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')


class RelationTests(TestListAPIViewMixin, DomainTestCase):

    api_url_name = 'domain:relation'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
