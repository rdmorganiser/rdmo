from django.test import TestCase
from django.utils import translation

from apps.core.testing.mixins import *
from apps.accounts.testing.factories import UserFactory

from .factories import ProjectFactory, SnapshotFactory


class ProjectTests(TestModelViewMixin, TestModelStringMixin, TestCase):

    list_url_name = 'projects'
    retrieve_url_name = 'project'

    create_url_name = 'project_create'
    update_url_name = 'project_update'
    delete_url_name = 'project_delete'

    api_url_name = 'projects:project'

    def setUp(self):
        translation.activate('en')

        user = UserFactory()
        self.client.login(username='user', password='user')

        self.instance = ProjectFactory.create(owner=[user])

    def test_model_owner_string(self):
        self.assertIsNotNone(self.instance.owner_string())


class SnapshotTests(TestModelStringMixin, TestCase):

    def setUp(self):
        translation.activate('en')

        user = UserFactory()
        self.client.login(username='user', password='user')

        project = ProjectFactory.create(owner=[user])
        self.instance = SnapshotFactory.create(project=project)
