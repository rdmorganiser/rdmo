from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import translation

from apps.core.test_mixins import *

from .factories import ProjectFactory


class ProjectsTestCase(TestCase):
    fixtures = [
        'testing/accounts.json'
    ]


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
        user = User.objects.get(username='user')
        self.instance = ProjectFactory.create(owner=[user])

    def test_model_owner_string(self):
        self.assertIsNotNone(self.instance.owner_string())


class SnapshotTests(TestModelStringMixin, ProjectsTestCase):

    def setUp(self):
        translation.activate('en')
        self.client.login(username='user', password='user')
        user = User.objects.get(username='user')
        self.instance = ProjectFactory.create(owner=[user]).current_snapshot
