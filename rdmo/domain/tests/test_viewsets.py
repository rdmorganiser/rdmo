from django.test import TestCase

from test_generator.viewsets import (
    TestModelViewsetMixin,
    TestReadOnlyModelViewsetMixin,
    TestListViewsetMixin,
    TestDetailViewsetMixin,
    TestUpdateViewsetMixin,
    TestDeleteViewsetMixin
)

from rdmo.accounts.utils import set_group_permissions

from ..models import Attribute


class DomainViewsetTestCase(TestCase):

    fixtures = (
        'users.json',
        'groups.json',
        'accounts.json',
        'domain.json',
        'options.json',
    )

    users = (
        ('editor', 'editor'),
        ('reviewer', 'reviewer'),
        ('user', 'user'),
        ('api', 'api'),
        ('anonymous', None),
    )

    status_map = {
        'list_viewset': {
            'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 403
        },
        'detail_viewset': {
            'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 403
        },
        'create_viewset': {
            'editor': 201, 'reviewer': 403, 'api': 403, 'user': 403, 'anonymous': 403
        },
        'update_viewset': {
            'editor': 200, 'reviewer': 403, 'api': 403, 'user': 403, 'anonymous': 403
        },
        'delete_viewset': {
            'editor': 204, 'reviewer': 403, 'api': 403, 'user': 403, 'anonymous': 403
        }
    }

    @classmethod
    def setUpTestData(cls):
        set_group_permissions()


class AttributeTests(TestModelViewsetMixin, DomainViewsetTestCase):

    # get attributes and order them by level to delete the attributes at the bottom of the tree first
    instances = Attribute.objects.order_by('-level')
    url_names = {
        'viewset': 'internal-domain:attribute'
    }

    def _test_create_viewset(self, username):
        for instance in self.instances:
            instance.key += '_new'
            self.assert_create_viewset(username, data=self.get_instance_as_dict(instance))

    def _test_delete_viewset(self, username):
        for instance in self.instances:
            self.assert_delete_viewset(username, kwargs={
                'pk': instance.pk
            })


class AttributeAPITests(TestReadOnlyModelViewsetMixin, DomainViewsetTestCase):

    instances = Attribute.objects.all()
    url_names = {
        'viewset': 'api-v1-domain:attribute'
    }
