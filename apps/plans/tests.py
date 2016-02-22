from django.test import TestCase, Client
from django.utils import translation

from .models import *


def plans_setUp(test_case):
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


# class ModelTestCase(TestCase):

#     def setUp(self):
#         plans_setUp(self)
#         translation.activate('en')

#     def test_plan_str(self):
#         self.assertEqual('%s - %s' % (self.interview, self.template), self.plan.__str__())

#     def test_template_str(self):
#         self.assertEqual('', self.template.__str__())
