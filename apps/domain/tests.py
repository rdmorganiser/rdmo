from django.test import TestCase
from django.utils import translation

from apps.core.testing.mixins import *

from apps.conditions.models import Condition
from apps.options.models import OptionSet

from .models import *


class DomainTestCase(TestCase):

    fixtures = (
        'conditions.json',
        'domain.json',
        'options.json',
    )

    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')


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
        # get entities and order them by level to delete the entities at the bottom of the tree first
        self.instances = AttributeEntity.objects.filter(attribute=None).order_by('-level')


class AttributeTests(TestModelAPIViewMixin, DomainTestCase):

    api_url_name = 'domain:attribute'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instances = Attribute.objects.all()


class RangeTests(TestListAPIViewMixin, TestRetrieveAPIViewMixin, TestUpdateAPIViewMixin, TestDeleteAPIViewMixin, DomainTestCase):

    api_url_name = 'domain:range'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instances = Range.objects.all()


class VerboseNameTests(TestListAPIViewMixin, TestRetrieveAPIViewMixin, TestUpdateAPIViewMixin, TestDeleteAPIViewMixin, DomainTestCase):

    api_url_name = 'domain:verbosename'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instances = VerboseName.objects.all()


class ValueTypeTests(TestListAPIViewMixin, DomainTestCase):

    api_url_name = 'domain:valuestype'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')


class OptionSetTests(TestListAPIViewMixin, TestRetrieveAPIViewMixin, DomainTestCase):

    api_url_name = 'domain:optionset'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instances = OptionSet.objects.all()


class ConditionTests(TestListAPIViewMixin, TestRetrieveAPIViewMixin, DomainTestCase):

    api_url_name = 'options:condition'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instances = Condition.objects.all()
