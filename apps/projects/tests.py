from django.test import TestCase
from django.utils import translation
from django.core.urlresolvers import reverse

from apps.core.testing.mixins import (
    TestUpdateViewMixin,
    TestDeleteViewMixin,
    TestModelViewMixin,
    TestModelStringMixin,
    TestModelAPIViewMixin,
    TestReadOnlyModelAPIViewMixin
)

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


class ProjectTests(TestModelViewMixin, TestReadOnlyModelAPIViewMixin, TestModelStringMixin, ProjectsTestCase):
    instances = Project.objects.filter(pk=1)

    url_names = {
        'list': 'projects',
        'retrieve': 'project',
        'create': 'project_create',
        'update': 'project_update',
        'delete': 'project_delete',
        'export': 'project_export_xml'
    }
    status_map = {
        'list': {
            'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 200, 'anonymous': 302,
        },
        'retrieve': {
            'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 403, 'anonymous': 302
        },
        'create': {
            'get': {
                'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 200, 'anonymous': 302
            },
            'post': {
                'owner': 302, 'manager': 302, 'author': 302, 'guest': 302, 'user': 302, 'anonymous': 302
            }
        },
        'update': {
            'get': {
                'owner': 200, 'manager': 200, 'author': 403, 'guest': 403, 'user': 403, 'anonymous': 302
            },
            'post': {
                'owner': 302, 'manager': 302, 'author': 403, 'guest': 403, 'user': 403, 'anonymous': 302
            }
        },
        'delete': {
            'get': {
                'owner': 200, 'manager': 403, 'author': 403, 'guest': 403, 'user': 403, 'anonymous': 302
            },
            'post': {
                'owner': 302, 'manager': 403, 'author': 403, 'guest': 403, 'user': 403, 'anonymous': 302
            }
        },
        'export': {'owner': 200, 'manager': 403, 'author': 403, 'guest': 403, 'user': 403, 'anonymous': 302}
    }

    api_url_name = 'internal-projects:project'
    api_status_map = {
        'list': {'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 200, 'anonymous': 403},
        'retrieve': {'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 404, 'anonymous': 403}
    }

    def test_export(self):
        translation.activate(self.lang)

        for username, password in self.users:
            if password:
                self.client.login(username=username, password=password)

                for instance in self.instances:
                    url = reverse(self.url_names['export'], kwargs={'pk': instance.pk})
                    response = self.client.get(url)

                    try:
                        self.assertEqual(response.status_code, self.status_map['export'][username])
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
        'create': 'membership_create',
        'update': 'membership_update',
        'delete': 'membership_delete'
    }
    status_map = {
        'create': {
            'get': {
                'owner': 200, 'manager': 403, 'author': 403, 'guest': 403, 'user': 403, 'anonymous': 302
            },
            'post': {
                'owner': 302, 'manager': 403, 'author': 403, 'guest': 403, 'user': 403, 'anonymous': 302
            }
        },
        'update': {
            'get': {
                'owner': 200, 'manager': 403, 'author': 403, 'guest': 403, 'user': 403, 'anonymous': 302
            },
            'post': {
                'owner': 302, 'manager': 403, 'author': 403, 'guest': 403, 'user': 403, 'anonymous': 302
            }
        },
        'delete': {
            'get': {
                'owner': 200, 'manager': 403, 'author': 403, 'guest': 403, 'user': 403, 'anonymous': 302
            },
            'post': {
                'owner': 302, 'manager': 403, 'author': 403, 'guest': 403, 'user': 403, 'anonymous': 302
            }
        }
    }

    def test_create_view_post(self):
        translation.activate(self.lang)

        for username, password in self.users:
            if password:
                self.client.login(username=username, password=password)

            for role in ['owner', 'manager', 'author', 'guest']:
                url = reverse(self.url_names['create'], args=[self.project_id])
                data = {
                    'username_or_email': 'user',
                    'role': role
                }
                response = self.client.post(url, data)

                try:
                    self.assertEqual(response.status_code, self.status_map['create']['post'][username])
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


class ValueTests(TestModelAPIViewMixin, ProjectsTestCase):

    project_id = 1

    instances = Value.objects.filter(project__pk=project_id)

    api_url_name = 'internal-projects:value'
    api_status_map = {
        'list': {'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 403, 'anonymous': 403},
        'retrieve': {'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 403, 'anonymous': 403},
        'create': {'owner': 201, 'manager': 201, 'author': 201, 'guest': 403, 'user': 403, 'anonymous': 403},
        'update': {'owner': 200, 'manager': 200, 'author': 200, 'guest': 403, 'user': 403, 'anonymous': 403},
        'delete': {'owner': 204, 'manager': 204, 'author': 204, 'guest': 403, 'user': 403, 'anonymous': 403}
    }

    def get_list_api_query_params(self):
        return {'project': self.project_id}

    def get_retrieve_api_query_params(self, instance):
        return {'project': self.project_id}

    def get_create_api_query_params(self):
        return {'project': self.project_id, 'foo': 'bar'}

    def get_update_api_query_params(self, instance):
        return {'project': self.project_id}

    def get_delete_api_query_params(self, instance):
        return {'project': self.project_id}


class QuestionEntityTests(TestReadOnlyModelAPIViewMixin, ProjectsTestCase):

    instances = QuestionEntity.objects.filter(question__parent=None)

    api_url_name = 'internal-projects:entity'
    api_status_map = {
        'list': {'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 200, 'anonymous': 403},
        'retrieve': {'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 200, 'anonymous': 403}
    }


class CatalogTests(TestReadOnlyModelAPIViewMixin, ProjectsTestCase):

    instances = Catalog.objects.all()

    api_url_name = 'internal-projects:catalog'
    api_status_map = {
        'list': {'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 200, 'anonymous': 403},
        'retrieve': {'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 200, 'anonymous': 403}
    }
