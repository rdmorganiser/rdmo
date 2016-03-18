from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.utils import translation

from apps.core.tests import TestListViewMixin, TestRetrieveViewMixin
from apps.core.tests import TestCreateViewMixin, TestUpdateViewMixin, TestDeleteViewMixin
from apps.core.tests import TestModelStringMixin

from .models import Project


class ProjectsTestCase(TestCase):
    fixtures = ['accounts/testing.json', 'domain/testing.json', 'questions/testing.json']


class ProjectTests(TestListViewMixin, TestRetrieveViewMixin,
                   TestCreateViewMixin, TestUpdateViewMixin, TestDeleteViewMixin,
                   TestModelStringMixin, ProjectsTestCase):

    list_url_name = 'projects'
    retrieve_url_name = 'project'

    create_url_name = 'project_create'
    update_url_name = 'project_update'
    delete_url_name = 'project_delete'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='user', password='user')
        self.instance = Project.objects.get(title='Project')
