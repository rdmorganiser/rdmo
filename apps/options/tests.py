from django.test import TestCase
from django.utils import translation

from apps.core.testing.mixins import *

from apps.conditions.models import Condition

from .models import *


class OptionsTestCase(TestCase):

    fixtures = (
        'conditions.json',
        'domain.json',
        'options.json'
    )

    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')


class OptionsTests(TestListViewMixin, OptionsTestCase):

    list_url_name = 'options'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')


class OptionSetTests(TestModelAPIViewMixin, OptionsTestCase):

    api_url_name = 'options:optionset'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instances = OptionSet.objects.all()

    def prepare_create_instance(self, instance):
        instance.identifier += '_new'
        return instance


class OptionTests(TestModelAPIViewMixin, OptionsTestCase):

    api_url_name = 'options:option'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instances = Option.objects.all()

    def prepare_create_instance(self, instance):
        instance.identifier += '_new'
        return instance


class ConditionTests(TestListAPIViewMixin, TestRetrieveAPIViewMixin, OptionsTestCase):

    api_url_name = 'options:condition'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instances = Condition.objects.all()
