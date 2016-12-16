from django.test import TestCase
from django.utils import translation

from apps.core.testing.mixins import *

from .models import *


class ViewsTestCase(TestCase):

    fixtures = (
        'conditions.json',
        'domain.json',
        'options.json',
        'views.json'
    )

    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')


class ViewsTests(TestListViewMixin, ViewsTestCase):

    list_url_name = 'views'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')


class ViewTests(TestModelAPIViewMixin, ViewsTestCase):

    api_url_name = 'views:view'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instances = View.objects.all()

    def prepare_create_instance(self, instance):
        instance.identifier += '_new'
        return instance
