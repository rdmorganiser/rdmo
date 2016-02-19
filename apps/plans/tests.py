# from django.test import TestCase, Client
# from django.utils import translation

# from apps.interviews.tests import interviews_setUp

# from .models import Plan, Template


# def plans_setUp(test_case):
#     interviews_setUp(test_case)

#     test_case.template = Template.objects.create()

#     test_case.plan = Plan.objects.create(
#         interview=test_case.interview,
#         template=test_case.template
#     )

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
