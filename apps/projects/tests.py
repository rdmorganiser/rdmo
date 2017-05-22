from django.test import TestCase
from django.utils import translation
from django.core.urlresolvers import reverse

from test_mixins.core import TestModelStringMixin
from test_mixins.views import TestUpdateViewMixin, TestDeleteViewMixin, TestModelViewMixin
from test_mixins.viewsets import TestModelViewsetMixin, TestReadOnlyModelViewsetMixin

from apps.accounts.utils import set_group_permissions
from apps.questions.models import Catalog, QuestionEntity

from .models import Project, Membership, Value


class ProjectsTestCase(TestCase):

    lang = 'en'

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

    def setUp(self):
        set_group_permissions()


class ProjectTests(TestModelViewMixin, TestReadOnlyModelViewsetMixin, TestModelStringMixin, ProjectsTestCase):
    instances = Project.objects.filter(pk=1)

    url_names = {
        'list_view': 'projects',
        'retrieve_view': 'project',
        'create_view': 'project_create',
        'update_view': 'project_update',
        'delete_view': 'project_delete',
        'export_view': 'project_export_xml',
        'viewset': 'internal-projects:project'
    }
    status_map = {
        'list_view': {
            'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 200, 'anonymous': 302,
        },
        'retrieve_view': {
            'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 403, 'anonymous': 302
        },
        'create_view_get': {
            'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 200, 'anonymous': 302
        },
        'create_view_post': {
            'owner': 302, 'manager': 302, 'author': 302, 'guest': 302, 'user': 302, 'anonymous': 302
        },
        'update_view_get': {
            'owner': 200, 'manager': 200, 'author': 403, 'guest': 403, 'user': 403, 'anonymous': 302
        },
        'update_view_post': {
            'owner': 302, 'manager': 302, 'author': 403, 'guest': 403, 'user': 403, 'anonymous': 302
        },
        'delete_view_get': {
            'owner': 200, 'manager': 403, 'author': 403, 'guest': 403, 'user': 403, 'anonymous': 302
        },
        'delete_view_post': {
            'owner': 302, 'manager': 403, 'author': 403, 'guest': 403, 'user': 403, 'anonymous': 302
        },
        'export_view': {
            'owner': 200, 'manager': 403, 'author': 403, 'guest': 403, 'user': 403, 'anonymous': 302
        },
        'list_viewset': {
            'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 200, 'anonymous': 403
        },
        'retrieve_viewset': {
            'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 404, 'anonymous': 403
        }
    }

    def test_export(self):
        translation.activate(self.lang)

        for username, password in self.users:
            if password:
                self.client.login(username=username, password=password)

                for instance in self.instances:
                    url = reverse(self.url_names['export_view'], kwargs={'pk': instance.pk})
                    response = self.client.get(url)

                    try:
                        self.assertEqual(response.status_code, self.status_map['export_view'][username])
                    except AssertionError:
                        print(
                            ('test', 'test_export'),
                            ('username', username),
                            ('url', url),
                            ('format', format),
                            ('status_code', response.status_code),
                            ('content', response.content)
                        )
                        raise

            self.client.logout()


class MembershipTests(TestUpdateViewMixin, TestDeleteViewMixin, TestModelStringMixin, ProjectsTestCase):

    project_id = 1

    instances = Membership.objects.filter(project__pk=project_id)

    url_names = {
        'create_view': 'membership_create',
        'update_view': 'membership_update',
        'delete_view': 'membership_delete'
    }
    status_map = {
        'create_view_get': {
            'owner': 200, 'manager': 403, 'author': 403, 'guest': 403, 'user': 403, 'anonymous': 302
        },
        'create_view_post': {
            'owner': 302, 'manager': 403, 'author': 403, 'guest': 403, 'user': 403, 'anonymous': 302
        },
        'update_view_get': {
            'owner': 200, 'manager': 403, 'author': 403, 'guest': 403, 'user': 403, 'anonymous': 302
        },
        'update_view_post': {
            'owner': 302, 'manager': 403, 'author': 403, 'guest': 403, 'user': 403, 'anonymous': 302
        },
        'delete_view_get': {
            'owner': 200, 'manager': 403, 'author': 403, 'guest': 403, 'user': 403, 'anonymous': 302
        },
        'delete_view_post': {
            'owner': 302, 'manager': 403, 'author': 403, 'guest': 403, 'user': 403, 'anonymous': 302
        }
    }

    def test_create_view_post(self):
        translation.activate(self.lang)

        for username, password in self.users:
            if password:
                self.client.login(username=username, password=password)

            for role in ['owner', 'manager', 'author', 'guest']:
                url = reverse(self.url_names['create_view'], args=[self.project_id])
                data = {
                    'username_or_email': 'user',
                    'role': role
                }
                response = self.client.post(url, data)

                try:
                    self.assertEqual(response.status_code, self.status_map['create_view_post'][username])
                    try:
                        Membership.objects.get(user__username='user', role=role).delete()
                    except Membership.DoesNotExist:
                        pass
                except AssertionError:
                    print(
                        ('test', 'test_create_view_post'),
                        ('username', username),
                        ('url', url),
                        ('data', data),
                        ('status_code', response.status_code),
                        ('content', response.content)
                    )
                    raise

            self.client.logout()

    def get_update_url_args(self, instance):
        return [self.project_id, instance.pk]

    def get_delete_url_args(self, instance):
        return [self.project_id, instance.pk]


class ValueTests(TestModelViewsetMixin, ProjectsTestCase):

    project_id = 1

    instances = Value.objects.filter(project__pk=project_id)

    url_names = {
        'viewset': 'internal-projects:value'
    }
    status_map = {
        'list_viewset': {'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 403, 'anonymous': 403},
        'retrieve_viewset': {'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 403, 'anonymous': 403},
        'create_viewset': {'owner': 201, 'manager': 201, 'author': 201, 'guest': 403, 'user': 403, 'anonymous': 403},
        'update_viewset': {'owner': 200, 'manager': 200, 'author': 200, 'guest': 403, 'user': 403, 'anonymous': 403},
        'delete_viewset': {'owner': 204, 'manager': 204, 'author': 204, 'guest': 403, 'user': 403, 'anonymous': 403}
    }

    def get_list_viewset_query_params(self):
        return {'project': self.project_id}

    def get_retrieve_viewset_query_params(self, instance):
        return {'project': self.project_id}

    def get_create_viewset_query_params(self):
        return {'project': self.project_id, 'foo': 'bar'}

    def get_update_viewset_query_params(self, instance):
        return {'project': self.project_id}

    def get_delete_viewset_query_params(self, instance):
        return {'project': self.project_id}


class QuestionEntityTests(TestReadOnlyModelViewsetMixin, ProjectsTestCase):

    instances = QuestionEntity.objects.filter(question__parent=None)

    url_names = {
        'viewset': 'internal-projects:entity'
    }
    status_map = {
        'list_viewset': {
            'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 200, 'anonymous': 403
        },
        'retrieve_viewset': {
            'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 200, 'anonymous': 403
        }
    }


class CatalogTests(TestReadOnlyModelViewsetMixin, ProjectsTestCase):

    instances = Catalog.objects.all()

    url_names = {
        'viewset': 'internal-projects:catalog'
    }
    status_map = {
        'list_viewset': {
            'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 200, 'anonymous': 403
        },
        'retrieve_viewset': {
            'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 200, 'anonymous': 403
        }
    }
