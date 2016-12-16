from django.test import TestCase
from django.utils import translation

from apps.core.testing.mixins import *

from apps.domain.models import Attribute

from .models import *


class ConditionsTestCase(TestCase):

    fixtures = (
        'conditions.json',
        'domain.json',
        'options.json'
    )

    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')


class ConditionsTests(TestListViewMixin, ConditionsTestCase):

    list_url_name = 'conditions'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')


class ConditionTests(TestModelAPIViewMixin, ConditionsTestCase):

    api_url_name = 'conditions:condition'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instances = Condition.objects.all()

    def prepare_create_instance(self, instance):
        instance.identifier += '_new'
        return instance


class AttributeTests(TestListAPIViewMixin, ConditionsTestCase):

    api_url_name = 'conditions:attribute'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instances = Attribute.objects.all()


class RelationTests(TestListAPIViewMixin, ConditionsTestCase):

    api_url_name = 'conditions:relation'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
