from django.test import TestCase
from django.utils import translation

from apps.core.testing.mixins import (
    TestListViewMixin,
    TestModelAPIViewMixin,
    TestListAPIViewMixin
)

from apps.domain.models import Attribute

from .models import Condition


class ConditionsTestCase(TestCase):

    fixtures = (
        'auth.json',
        'accounts.json',
        'conditions.json',
        'domain.json',
        'options.json',
    )


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
        instance.key += '_new'
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
