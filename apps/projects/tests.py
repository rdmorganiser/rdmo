from django.test import TestCase
from django.utils import translation

from apps.core.tests import TestListViewMixin
from apps.core.tests import TestRetrieveViewMixin
from apps.core.tests import TestCreateViewMixin
from apps.core.tests import TestUpdateViewMixin
from apps.core.tests import TestDeleteViewMixin
from apps.core.tests import TestModelStringMixin

from .models import Project


class ProjectsTestCase(TestCase):
    fixtures = ['accounts/testing.json', 'domain/testing.json', 'questions/testing.json', 'projects/testing.json']


class ProjectTests(TestListViewMixin,
                   TestRetrieveViewMixin,
                   TestCreateViewMixin,
                   TestUpdateViewMixin,
                   TestDeleteViewMixin,
                   TestModelStringMixin,
                   ProjectsTestCase):

    list_url_name = 'projects'
    retrieve_url_name = 'project'

    create_url_name = 'project_create'
    update_url_name = 'project_update'
    delete_url_name = 'project_delete'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='user', password='user')
        self.instance = Project.objects.get(title='Project')

    def test_model_owner_string(self):
        self.assertIsNotNone(self.instance.owner_string())


class SnapshotTests(TestModelStringMixin,
                    ProjectsTestCase):

    def setUp(self):
        translation.activate('en')
        self.client.login(username='user', password='user')
        self.instance = Project.objects.get(title='Project').current_snapshot
