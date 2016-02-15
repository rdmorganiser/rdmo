from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import translation

from .models import Project


def projects_setUp(test_case):
    test_case.user = User.objects.create_user('user', 'user@example.com', 'password')

    test_case.project = Project(
        name='test_name',
        pi='test_pi',
        description='test_description'
    )
    test_case.project.save()
    test_case.project.owner.add(test_case.user)
    test_case.project.save()


class ClientTestCase(TestCase):

    def setUp(self):
        projects_setUp(self)
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

    def test_project_create(self):
        """ A project can be created. """

        # get the url
        url = reverse('project_create')

        # get the client object and log in
        client = Client()
        client.login(username='user', password='password')

        # access the page
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

        # try to post to the form
        response = client.post(url, {
            'name': 'test',
            'pi': 'Tom Test',
            'description': '',
        })
        self.assertEqual(response.status_code, 302)

    def test_project_update(self):
        """ A project can be created. """

        # get the url
        url = reverse('project_update', args=[self.project.pk])

        # get the client object and log in
        client = Client()
        client.login(username='user', password='password')

        # access the page
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

        # try to post to the form
        response = client.post(url, {
            'name': 'test1',
            'pi': 'Tom Test',
            'description': '',
        })
        self.assertEqual(response.status_code, 302)

    def test_project_delete(self):
        """ A project can be created. """

        # get the url
        url = reverse('project_delete', args=[self.project.pk])

        # get the client object and log in
        client = Client()
        client.login(username='user', password='password')

        # access the page
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

        # try to post to the form
        response = client.post(url, {})
        self.assertEqual(response.status_code, 302)


class ModelTestCase(TestCase):

    def setUp(self):
        projects_setUp(self)
        translation.activate('en')

    def test_project_str(self):
        self.assertEqual('test_name', self.project.__str__())
