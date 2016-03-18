from django.test import TestCase
from django.utils import translation

from apps.core.tests import TestListViewMixin
from apps.core.tests import TestCreateViewMixin, TestUpdateViewMixin, TestDeleteViewMixin
from apps.core.tests import TestModelStringMixin

from .models import Attribute, AttributeSet


class DomainTestCase(TestCase):
    fixtures = ['accounts/testing.json', 'domain/testing.json']


class DomainTests(TestListViewMixin, DomainTestCase):

    list_url_name = 'domain'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='user', password='user')


class AttributeTests(TestCreateViewMixin, TestUpdateViewMixin, TestDeleteViewMixin,
                     TestModelStringMixin, DomainTestCase):

    create_url_name = 'attribute_create'
    update_url_name = 'attribute_update'
    delete_url_name = 'attribute_delete'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='user', password='user')
        self.instance = Attribute.objects.get(tag='attribute')


class AttributeSetTests(TestCreateViewMixin, TestUpdateViewMixin, TestDeleteViewMixin,
                        TestModelStringMixin, DomainTestCase):

    create_url_name = 'attributeset_create'
    update_url_name = 'attributeset_update'
    delete_url_name = 'attributeset_delete'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='user', password='user')
        self.instance = AttributeSet.objects.get(tag='attributeset')
