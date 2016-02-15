from django.test import TestCase, Client
from django.utils import translation

from apps.interviews.tests import interviews_setUp

from .models import Plan, Template


def plans_setUp(test_case):
    interviews_setUp(test_case)

    test_case.template = Template()
    test_case.template.save()

    test_case.plan = Plan(
        interview=test_case.interview,
        template=test_case.template
    )
    test_case.plan.save()


class ClientTestCase(TestCase):

    def setUp(self):
        plans_setUp(self)
        translation.activate('en')


class ModelTestCase(TestCase):

    def setUp(self):
        plans_setUp(self)
        translation.activate('en')

    def test_plan_str(self):
        self.assertEqual('%s - %s' % (self.interview, self.template), self.plan.__str__())

    def test_template_str(self):
        self.assertEqual('', self.template.__str__())
