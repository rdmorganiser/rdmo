from django.test import TestCase
from django.core.urlresolvers import reverse

from test_generator.core import TestModelStringMixin
from test_generator.views import TestModelViewMixin, TestViewMixin

from rdmo.accounts.utils import set_group_permissions

from ..models import Project, Membership


class ProjectsViewTestCase(TestCase):

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


class ProjectTests(TestModelViewMixin, TestModelStringMixin, ProjectsViewTestCase):

    instances = Project.objects.filter(pk=1)

    url_names = {
        'list_view': 'projects',
        'detail_view': 'project',
        'create_view': 'project_create',
        'update_view': 'project_update',
        'delete_view': 'project_delete',
        'export_view': 'project_export_xml',
    }

    status_map = {
        'list_view': {
            'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 200, 'anonymous': 302,
        },
        'detail_view': {
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
        }
    }

    def _test_export(self, username):
        for instance in self.instances:

            url = reverse(self.url_names['export_view'], kwargs={'pk': instance.pk})
            response = self.client.get(url)

            self.assertEqual(response.status_code, self.status_map['export_view'][username], msg=(
                ('username', username),
                ('url', url),
                ('status_code', response.status_code),
                ('content', response.content)
            ))


class MembershipTests(TestViewMixin, TestModelStringMixin, ProjectsViewTestCase):

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

    def _test_create_view_get(self, username):
        self.assert_create_view_get(username, {
            'project_id': self.project_id
        })

    def _test_create_view_post(self, username):

        for role in ['owner', 'manager', 'author', 'guest']:

            url = reverse(self.url_names['create_view'], kwargs={'project_id': self.project_id})
            data = {
                'username_or_email': 'user',
                'role': role
            }
            response = self.client.post(url, data)

            self.assertEqual(response.status_code, self.status_map['create_view_post'][username], msg=(
                ('username', username),
                ('url', url),
                ('data', data),
                ('status_code', response.status_code),
                ('content', response.content)
            ))

            try:
                Membership.objects.get(user__username='user', role=role).delete()
            except Membership.DoesNotExist:
                pass

    def _test_update_view_get(self, username):
        for instance in self.instances:
            self.assert_update_view_get(username, {
                'project_id': self.project_id,
                'pk': instance.pk
            })

    def _test_update_view_post(self, username):
        for instance in self.instances:
            data = self.get_instance_as_dict(instance)
            self.assert_update_view_post(username, {
                'project_id': self.project_id,
                'pk': instance.pk
            }, data)

    def _test_delete_view_get(self, username):
        for instance in self.instances:
            self.assert_delete_view_get(username, {
                'project_id': self.project_id,
                'pk': instance.pk
            })

    def _test_delete_view_post(self, username):
        for instance in self.instances:
            self.assert_delete_view_post(username, {
                'project_id': self.project_id,
                'pk': instance.pk
            })
            instance.save(update_fields=None)
