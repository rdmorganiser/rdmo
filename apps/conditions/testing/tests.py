from django.test import TestCase
from django.utils import translation

from apps.core.testing.mixins import *
from apps.accounts.testing.factories import AdminFactory
from apps.domain.testing.factories import AttributeFactory


from .factories import *


class ConditionsTests(TestListViewMixin, TestCase):

    list_url_name = 'conditions'

    def setUp(self):
        translation.activate('en')

        AdminFactory()
        self.client.login(username='admin', password='admin')


class ConditionTests(TestModelAPIViewMixin, TestCase):

    api_url_name = 'conditions:condition'

    def setUp(self):
        translation.activate('en')

        AdminFactory()
        self.client.login(username='admin', password='admin')

        self.instance = ConditionFactory()


class AttributeTests(TestModelAPIViewMixin, TestCase):

    api_url_name = 'conditions:attribute'

    def setUp(self):
        translation.activate('en')

        AdminFactory()
        self.client.login(username='admin', password='admin')

        self.instance = AttributeFactory()


class RelationTests(TestListAPIViewMixin, TestCase):

    api_url_name = 'conditions:relation'

    def setUp(self):
        translation.activate('en')

        AdminFactory()
        self.client.login(username='admin', password='admin')
