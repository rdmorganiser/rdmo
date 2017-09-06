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

from rdmo.conditions.models import Condition
from rdmo.options.models import OptionSet

from ..models import AttributeEntity, Attribute, Range, VerboseName


class DomainViewsetTestCase(TestCase):

    fixtures = (
        'users.json',
        'groups.json',
        'accounts.json',
        'conditions.json',
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


class AttributeEntityTests(TestModelViewsetMixin, DomainViewsetTestCase):

    # get entities and order them by level to delete the entities at the bottom of the tree first
    instances = AttributeEntity.objects.filter(attribute=None).order_by('-level')
    url_names = {
        'viewset': 'internal-domain:entity'
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


class AttributeTests(TestModelViewsetMixin, DomainViewsetTestCase):

    instances = Attribute.objects.all()
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


class RangeTests(TestListViewsetMixin, TestDetailViewsetMixin, TestUpdateViewsetMixin, TestDeleteViewsetMixin, DomainViewsetTestCase):

    instances = Range.objects.all()
    url_names = {
        'viewset': 'internal-domain:range'
    }


class VerboseNameTests(TestListViewsetMixin, TestDetailViewsetMixin, TestUpdateViewsetMixin, TestDeleteViewsetMixin, DomainViewsetTestCase):

    instances = VerboseName.objects.all()
    url_names = {
        'viewset': 'internal-domain:verbosename'
    }


class ValueTypeTests(TestListViewsetMixin, DomainViewsetTestCase):

    url_names = {
        'viewset': 'internal-domain:valuestype'
    }
    status_map = {
        'list_viewset': {
            'editor': 200, 'reviewer': 200, 'reviewer': 200, 'api': 200, 'user': 200, 'anonymous': 403
        }
    }


class OptionSetTests(TestReadOnlyModelViewsetMixin, DomainViewsetTestCase):

    instances = OptionSet.objects.all()
    url_names = {
        'viewset': 'internal-domain:optionset'
    }


class ConditionTests(TestReadOnlyModelViewsetMixin, DomainViewsetTestCase):

    instances = Condition.objects.all()
    url_names = {
        'viewset': 'internal-domain:condition'
    }


class AttributeEntityAPITests(TestReadOnlyModelViewsetMixin, DomainViewsetTestCase):

    instances = AttributeEntity.objects.filter(attribute=None)
    url_names = {
        'viewset': 'api-v1-domain:entity'
    }


class AttributeAPITests(TestReadOnlyModelViewsetMixin, DomainViewsetTestCase):

    instances = Attribute.objects.all()
    url_names = {
        'viewset': 'api-v1-domain:attribute'
    }
