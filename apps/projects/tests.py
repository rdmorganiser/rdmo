from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.utils import translation

from .models import Project


class ClientTestCase(TestCase):
    fixtures = ['accounts/testing.json', 'domain/testing.json', 'catalogs/testing.json', 'projects/testing.json']

    def setUp(self):
        translation.activate('en')

        self.project = Project.objects.get(title='Title')

    def test_projects(self):
        """
        The projects page can be accessed.
        """
        client = Client()
        client.login(username='user', password='user')

        response = client.get(reverse('projects'))
        self.assertEqual(response.status_code, 200)

    def test_project(self):
        """
        The project page can be accessed.
        """
        client = Client()
        client.login(username='user', password='user')

        url = reverse('project', args=[self.project.pk])
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_project_create(self):
        """
        A GET request to the project create form returns the form.
        """
        client = Client()
        client.login(username='user', password='user')

        url = reverse('project_create')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_project_create(self):
        """
        A POST request to the project create form creates a project.
        """
        client = Client()
        client.login(username='user', password='user')

        url = reverse('project_create')
        response = client.post(url, {
            'title': 'Other title',
            'description': '',
            'catalog': 1
        })
        self.assertEqual(response.status_code, 302)

        other_project = Project.objects.get(title='Other title')
        self.assertIsNotNone(other_project)

    def test_get_project_update(self):
        """
        A GET request to the project update form returns the form.
        """
        client = Client()
        client.login(username='user', password='user')

        url = reverse('project_update', args=[self.project.pk])
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_project_update(self):
        """
        A POST request to the project update form creates a project.
        """
        client = Client()
        client.login(username='user', password='user')

        url = reverse('project_update', args=[self.project.pk])
        response = client.post(url, {
            'title': 'Other title',
            'description': '',
            'catalog': 1
        })
        self.assertEqual(response.status_code, 302)

        other_project = Project.objects.get(title='Other title')
        self.assertEqual(other_project.pk, self.project.pk)

    def test_get_project_delete(self):
        """
        A GET request to the project delete form returns the form.
        """
        client = Client()
        client.login(username='user', password='user')

        url = reverse('project_delete', args=[self.project.pk])
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_project_delet(self):
        """
        A POST request to the project delete form deletes a project.
        """
        client = Client()
        client.login(username='user', password='user')

        url = reverse('project_delete', args=[self.project.pk])
        response = client.post(url, {})
        self.assertEqual(response.status_code, 302)

        with self.assertRaises(Project.DoesNotExist):
            Project.objects.get(title=self.project.title)


class ModelTestCase(TestCase):
    fixtures = ['accounts/testing.json', 'domain/testing.json', 'catalogs/testing.json', 'projects/testing.json']

    def setUp(self):
        translation.activate('en')
        self.project = Project.objects.get(title='Title')

    def test_project_str(self):
        self.assertEqual(self.project.title, self.project.__str__())
