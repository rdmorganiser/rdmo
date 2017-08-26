from django.test import TestCase

from test_generator.core import TestSingleObjectMixin, TestModelStringMixin
from test_generator.viewsets import TestReadOnlyModelViewsetMixin, TestViewsetMixin

from rdmo.accounts.utils import set_group_permissions
from rdmo.questions.models import Catalog, QuestionEntity

from ..models import Project, Value


class ProjectsViewsetTestCase(TestCase):

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

    users = (
        ('owner', 'owner'),
        ('manager', 'manager'),
        ('author', 'author'),
        ('guest', 'guest'),
        ('user', 'user'),
        ('anonymous', None),
    )

    @classmethod
    def setUpTestData(cls):
        set_group_permissions()


class ProjectTests(TestReadOnlyModelViewsetMixin, TestModelStringMixin, ProjectsViewsetTestCase):

    instances = Project.objects.filter(pk=1)

    url_names = {
        'viewset': 'internal-projects:project'
    }

    status_map = {
        'list_viewset': {
            'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 200, 'anonymous': 403
        },
        'detail_viewset': {
            'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 404, 'anonymous': 403
        }
    }


class ValueTests(TestViewsetMixin, TestSingleObjectMixin, ProjectsViewsetTestCase):

    project_id = 1
    instances = Value.objects.filter(project__pk=project_id)

    url_names = {
        'viewset': 'internal-projects:value'
    }

    status_map = {
        'list_viewset': {
            'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 403, 'anonymous': 403
        },
        'detail_viewset': {
            'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 403, 'anonymous': 403
        },
        'create_viewset': {
            'owner': 201, 'manager': 201, 'author': 201, 'guest': 403, 'user': 403, 'anonymous': 403
        },
        'update_viewset': {
            'owner': 200, 'manager': 200, 'author': 200, 'guest': 403, 'user': 403, 'anonymous': 403
        },
        'delete_viewset': {
            'owner': 204, 'manager': 204, 'author': 204, 'guest': 403, 'user': 403, 'anonymous': 403
        }
    }

    def _test_list_viewset(self, username):
        self.assert_list_viewset(username, query_params={
                'project': self.project_id
            })

    def _test_create_viewset(self, username):
        for instance in self.instances:
            self.assert_create_viewset(username, data=self.get_instance_as_dict(instance), query_params={
                'project': self.project_id
            })

    def _test_detail_viewset(self, username):
        for instance in self.instances:
            self.assert_detail_viewset(username, kwargs={
                'pk': instance.pk
            }, query_params={
                'project': self.project_id
            })

    def _test_update_viewset(self, username):
        for instance in self.instances:
            self.assert_update_viewset(username, kwargs={
                'pk': instance.pk
            }, data=self.get_instance_as_dict(instance), query_params={
                'project': self.project_id
            })

    def _test_delete_viewset(self, username):
        for instance in self.instances:
            self.assert_delete_viewset(username, kwargs={
                'pk': instance.pk
            }, query_params={
                'project': self.project_id
            })
            instance.save(update_fields=None)


class QuestionEntityTests(TestReadOnlyModelViewsetMixin, ProjectsViewsetTestCase):

    instances = QuestionEntity.objects.filter(question__parent=None)

    url_names = {
        'viewset': 'internal-projects:entity'
    }

    status_map = {
        'list_viewset': {
            'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 200, 'anonymous': 403
        },
        'detail_viewset': {
            'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 200, 'anonymous': 403
        }
    }


class CatalogTests(TestReadOnlyModelViewsetMixin, ProjectsViewsetTestCase):

    instances = Catalog.objects.all()

    url_names = {
        'viewset': 'internal-projects:catalog'
    }

    status_map = {
        'list_viewset': {
            'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 200, 'anonymous': 403
        },
        'detail_viewset': {
            'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 200, 'anonymous': 403
        }
    }
