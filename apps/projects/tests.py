import re

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import translation

from .models import Project


class ClientTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('user', 'user@example.com', 'password')
        self.project = Project(
            name='Test',
            pi='Tom Test',
            description='This is a Test.'
        )
        self.project.save()
        self.project.owner.add(self.user)
        self.project.save()
        translation.activate('en')

    def test_projects(self):
        """ The projects page can be accessed. """

        # get the client object and log in
        client = Client()
        client.login(username='user', password='password')

        # access the page
        response = client.get(reverse('projects'))
        self.assertEqual(response.status_code, 200)

    def test_project(self):
        """ The project page can be accessed. """

        # get the client object and log in
        client = Client()
        client.login(username='user', password='password')

        # access the page
        response = client.get(reverse('project', args=[self.project.pk]))
        self.assertEqual(response.status_code, 200)


class ModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('test', 'test@example.com', 'test')

    def test_project_str(self):
        project = Project(
            name='Test',
            pi='Tom Test',
            description='This is a Test.'
        )
        project.save()
        self.assertEqual(project.name, project.__str__())
