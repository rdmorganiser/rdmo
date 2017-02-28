from django.test import TestCase
from django.utils import translation

from apps.core.testing.mixins import (
    TestModelViewMixin,
    TestModelStringMixin
)

from .models import Project, Snapshot


class ProjectsTestCase(TestCase):

    fixtures = (
        'users.json',
        'groups.json',
        'accounts.json',
        'conditions.json',
        'domain.json',
        'options.json',
        'questions.json',
        'tasks.json',
        'views.json',
        'projects.json',
    )


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
        self.instances = Project.objects.filter(user__username='user')


class SnapshotTests(TestModelStringMixin, ProjectsTestCase):

    def setUp(self):
        translation.activate('en')
        self.client.login(username='user', password='user')
        self.instances = Snapshot.objects.filter(project__user__username='user')
