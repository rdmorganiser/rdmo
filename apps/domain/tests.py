from django.test import TestCase, Client
from django.utils import translation

from .models import Attribute, AttributeSet


class ClientTestCase(TestCase):
    fixtures = ['domain/testing.json']

    def setUp(self):
        translation.activate('en')


class ModelTestCase(TestCase):
    fixtures = ['domain/testing.json']

    def setUp(self):
        translation.activate('en')
        self.attribute = Attribute.objects.get(tag='attribute')
        self.attributeset = AttributeSet.objects.get(tag='attributeset')
        self.attributeset_attribute = Attribute.objects.get(tag='attributeset_attribute')

    def test_attribute(self):
        self.assertEqual(self.attribute.tag, self.attribute.__str__())
        self.assertEqual('%s.%s' % (self.attributeset.tag, self.attributeset_attribute.tag), self.attributeset_attribute.__str__())

    def test_attributeset(self):
        self.assertEqual(self.attributeset.tag, self.attributeset.__str__())

    # def test_template(self):
    #     self.assertEqual(self.template.__str__(), '')
