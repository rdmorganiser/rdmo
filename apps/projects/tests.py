from django.test import TestCase
from django.utils import translation

from apps.core.testing.mixins import *

from .models import *


class ProjectsTestCase(TestCase):

    fixtures = (
        'auth.json',
        'accounts.json',
        'conditions.json',
        'domain.json',
        'options.json',
        'questions.json',
        'tasks.json',
        'views.json',
        'projects.json',
    )

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user('user', 'user@example.com', 'user')


class ProjectTests(TestModelViewMixin, TestModelStringMixin, ProjectsTestCase):

    list_url_name = 'projects'
    retrieve_url_name = 'project'

    create_url_name = 'project_create'
    update_url_name = 'project_update'
    delete_url_name = 'project_delete'

    api_url_name = 'projects:project'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='user', password='user')
        self.instances = Project.objects.filter(owner__username='user')

    def test_model_owner_string(self):
        for instance in self.instances:
            self.assertIsNotNone(instance.owner_string())


class SnapshotTests(TestModelStringMixin, ProjectsTestCase):

    def setUp(self):
        translation.activate('en')
        self.client.login(username='user', password='user')
        self.instances = Snapshot.objects.filter(project__owner__username='user')
