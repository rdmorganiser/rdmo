from django.test import TestCase, Client
from django.utils import translation

from .models import *


def domain_setUp(test_case):
    test_case.attribute = Attribute.objects.create(tag='test_tag')
    test_case.attributeset = AttributeSet.objects.create(tag='test_tag')

    Attribute.objects.create(
        tag='test_tag',
        attributeset=test_case.attributeset
    )

    test_case.template = Template.objects.create()

# class ClientTestCase(TestCase):

#     def setUp(self):
#         plans_setUp(self)
#         translation.activate('en')


class ModelTestCase(TestCase):

    def setUp(self):
        domain_setUp(self)
        translation.activate('en')

    def test_attribute(self):
        self.assertEqual(self.attribute.__str__(), 'test_tag')
        self.assertEqual(self.attributeset.attributes.first().__str__(), 'test_tag.test_tag')

    def test_attributeset(self):
        self.assertEqual(self.attributeset.__str__(), 'test_tag')

    def test_template(self):
        self.assertEqual(self.template.__str__(), '')
