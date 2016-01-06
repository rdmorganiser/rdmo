from datetime import datetime

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import translation

from apps.projects.models import Project
from apps.interviews.models import Interview

from .models import Plan, Template


# class ClientTestCase(TestCase):

#     def setUp(self):
#         self.user = User.objects.create_user('user', 'user@example.com', 'password')


class ModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('test', 'test@example.com', 'test')

        self.project = Project(name='Test', pi='Tom Test', description='This is a Test.')
        self.project.save()
        self.project.owner.add(self.user)
        self.project.save()

        self.interview = Interview(project=self.project, title='Title', date=datetime.now())
        self.interview.save()

        self.template = Template()
        self.template.save()

        self.plan = Plan(interview=self.interview, template=self.template)
        self.plan.save()

    def test_plan_str(self):
        self.assertEqual('%s - %s' % (self.interview, self.template), self.plan.__str__())

    def test_template_str(self):
        self.assertEqual('', self.template.__str__())
