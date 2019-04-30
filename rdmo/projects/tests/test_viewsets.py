from django.test import TestCase

from test_generator.core import TestSingleObjectMixin, TestModelStringMixin
from test_generator.viewsets import TestModelViewsetMixin, TestReadOnlyModelViewsetMixin, TestViewsetMixin

from rdmo.accounts.utils import set_group_permissions
from rdmo.questions.models import Catalog, QuestionSet

from ..models import Project, Snapshot, Value


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
        ('api', 'api'),
        ('user', 'user'),
        ('anonymous', None),
    )

    @classmethod
    def setUpTestData(cls):
        set_group_permissions()


class ProjectTests(TestModelViewsetMixin, TestModelStringMixin, ProjectsViewsetTestCase):

    project_id = 1
    instances = Project.objects.filter(pk=project_id)

    url_names = {
        'viewset': 'v1-projects:project'
    }

    status_map = {
        'list_viewset': {
            'owner': 403, 'manager': 403, 'author': 403, 'guest': 403, 'api': 200, 'user': 403, 'anonymous': 401
        },
        'detail_viewset': {
            'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'api': 200, 'user': 404, 'anonymous': 401
        },
        'create_viewset': {
            'owner': 403, 'manager': 403, 'author': 403, 'guest': 403, 'api': 201, 'user': 403, 'anonymous': 401
        },
        'update_viewset': {
            'owner': 200, 'manager': 200, 'author': 403, 'guest': 403, 'api': 200, 'user': 404, 'anonymous': 401
        },
        'delete_viewset': {
            'owner': 204, 'manager': 403, 'author': 403, 'guest': 403, 'api': 204, 'user': 404, 'anonymous': 401
        },
        'resolve_viewset': {
            'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'api': 200, 'user': 404, 'anonymous': 401
        }
    }

    def _test_resolve_viewset(self, username):
        for instance in self.instances:
            self.assert_viewset('resolve_viewset', 'get', 'resolve', username, kwargs={
                'pk': instance.id,
            }, query_params={
                'condition': 1
            })


class ProjectSnapshotTests(TestViewsetMixin, TestSingleObjectMixin, ProjectsViewsetTestCase):

    project_id = 1
    instances = Snapshot.objects.filter(project__pk=project_id)

    url_names = {
        'viewset': 'v1-projects:project-snapshot'
    }

    status_map = {
        'list_viewset': {
            'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'api': 200, 'user': 404, 'anonymous': 404
        },
        'detail_viewset': {
            'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'api': 200, 'user': 404, 'anonymous': 401
        },
        'create_viewset': {
            'owner': 201, 'manager': 201, 'author': 403, 'guest': 403, 'api': 201, 'user': 404, 'anonymous': 404
        },
        'update_viewset': {
            'owner': 200, 'manager': 200, 'author': 403, 'guest': 403, 'api': 200, 'user': 404, 'anonymous': 401
        },
        'delete_viewset': {
            'owner': 405, 'manager': 405, 'author': 405, 'guest': 405, 'api': 405, 'user': 405, 'anonymous': 401
        }
    }

    def _test_list_viewset(self, username):
        self.assert_list_viewset(username, kwargs={
            'parent_lookup_project': self.project_id
        })

    def _test_create_viewset(self, username):
        for instance in self.instances:
            self.assert_create_viewset(username, data=self.get_instance_as_dict(instance), kwargs={
                'parent_lookup_project': self.project_id,
            })

    def _test_detail_viewset(self, username):
        for instance in self.instances:
            self.assert_detail_viewset(username, kwargs={
                'parent_lookup_project': self.project_id,
                'pk': instance.pk
            })

    def _test_update_viewset(self, username):
        for instance in self.instances:
            self.assert_update_viewset(username, kwargs={
                'parent_lookup_project': self.project_id,
                'pk': instance.pk
            }, data=self.get_instance_as_dict(instance))

    def _test_delete_viewset(self, username):
        for instance in self.instances:
            self.assert_delete_viewset(username, kwargs={
                'parent_lookup_project': self.project_id,
                'pk': instance.pk
            })
            instance.save(update_fields=None)


class ProjectValueTests(TestViewsetMixin, TestSingleObjectMixin, ProjectsViewsetTestCase):

    project_id = 1
    instances = Value.objects.filter(project__pk=project_id, snapshot=None)

    url_names = {
        'viewset': 'v1-projects:project-value'
    }

    status_map = {
        'list_viewset': {
            'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'api': 200, 'user': 404, 'anonymous': 404
        },
        'detail_viewset': {
            'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'api': 200, 'user': 404, 'anonymous': 401
        },
        'create_viewset': {
            'owner': 201, 'manager': 201, 'author': 201, 'guest': 403, 'api': 201, 'user': 404, 'anonymous': 404
        },
        'update_viewset': {
            'owner': 200, 'manager': 200, 'author': 200, 'guest': 403, 'api': 200, 'user': 404, 'anonymous': 401
        },
        'delete_viewset': {
            'owner': 204, 'manager': 204, 'author': 204, 'guest': 403, 'api': 204, 'user': 404, 'anonymous': 401
        }
    }

    def _test_list_viewset(self, username):
        self.assert_list_viewset(username, kwargs={
            'parent_lookup_project': self.project_id
        })

    def _test_create_viewset(self, username):
        for instance in self.instances:
            self.assert_create_viewset(username, data=self.get_instance_as_dict(instance), kwargs={
                'parent_lookup_project': self.project_id,
            })

    def _test_detail_viewset(self, username):
        for instance in self.instances:
            self.assert_detail_viewset(username, kwargs={
                'parent_lookup_project': self.project_id,
                'pk': instance.pk
            })

    def _test_update_viewset(self, username):
        for instance in self.instances:
            self.assert_update_viewset(username, kwargs={
                'parent_lookup_project': self.project_id,
                'pk': instance.pk
            }, data=self.get_instance_as_dict(instance))

    def _test_delete_viewset(self, username):
        for instance in self.instances:
            self.assert_delete_viewset(username, kwargs={
                'parent_lookup_project': self.project_id,
                'pk': instance.pk
            })
            instance.save(update_fields=None)


class SnapshotTests(TestModelViewsetMixin, TestModelStringMixin, ProjectsViewsetTestCase):

    instances = Snapshot.objects.all()

    url_names = {
        'viewset': 'v1-projects:snapshot'
    }

    status_map = {
        'list_viewset': {
            'owner': 403, 'manager': 403, 'author': 403, 'guest': 403, 'api': 200, 'user': 403, 'anonymous': 401
        },
        'detail_viewset': {
            'owner': 403, 'manager': 403, 'author': 403, 'guest': 403, 'api': 200, 'user': 403, 'anonymous': 401
        },
        'create_viewset': {
            'owner': 403, 'manager': 403, 'author': 403, 'guest': 403, 'api': 201, 'user': 403, 'anonymous': 401
        },
        'update_viewset': {
            'owner': 403, 'manager': 403, 'author': 403, 'guest': 403, 'api': 200, 'user': 403, 'anonymous': 401
        },
        'delete_viewset': {
            'owner': 403, 'manager': 403, 'author': 403, 'guest': 403, 'api': 405, 'user': 403, 'anonymous': 401
        }
    }


class ValueTests(TestModelViewsetMixin, TestModelStringMixin, ProjectsViewsetTestCase):

    instances = Value.objects.all()

    url_names = {
        'viewset': 'v1-projects:value'
    }

    status_map = {
        'list_viewset': {
            'owner': 403, 'manager': 403, 'author': 403, 'guest': 403, 'api': 200, 'user': 403, 'anonymous': 401
        },
        'detail_viewset': {
            'owner': 403, 'manager': 403, 'author': 403, 'guest': 403, 'api': 200, 'user': 403, 'anonymous': 401
        },
        'create_viewset': {
            'owner': 403, 'manager': 403, 'author': 403, 'guest': 403, 'api': 201, 'user': 403, 'anonymous': 401
        },
        'update_viewset': {
            'owner': 403, 'manager': 403, 'author': 403, 'guest': 403, 'api': 200, 'user': 403, 'anonymous': 401
        },
        'delete_viewset': {
            'owner': 403, 'manager': 403, 'author': 403, 'guest': 403, 'api': 204, 'user': 403, 'anonymous': 401
        }
    }


class QuestionSetTests(TestReadOnlyModelViewsetMixin, ProjectsViewsetTestCase):

    instances = QuestionSet.objects.all()

    url_names = {
        'viewset': 'v1-projects:questionset'
    }

    status_map = {
        'list_viewset': {
            'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'api': 200, 'user': 200, 'anonymous': 401
        },
        'detail_viewset': {
            'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'api': 200, 'user': 200, 'anonymous': 401
        }
    }


class CatalogTests(TestReadOnlyModelViewsetMixin, ProjectsViewsetTestCase):

    instances = Catalog.objects.all()

    url_names = {
        'viewset': 'v1-projects:catalog'
    }

    status_map = {
        'list_viewset': {
            'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'api': 200, 'user': 200, 'anonymous': 401
        },
        'detail_viewset': {
            'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'api': 200, 'user': 200, 'anonymous': 401
        }
    }
