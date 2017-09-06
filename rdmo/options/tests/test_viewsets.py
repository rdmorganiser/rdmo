from django.test import TestCase

from test_generator.viewsets import TestModelViewsetMixin, TestReadOnlyModelViewsetMixin

from rdmo.accounts.utils import set_group_permissions

from rdmo.conditions.models import Condition

from ..models import OptionSet, Option


class OptionsViewsetTestCase(TestCase):

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


class OptionSetTests(TestModelViewsetMixin, OptionsViewsetTestCase):

    instances = OptionSet.objects.all()
    url_names = {
        'viewset': 'internal-options:optionset'
    }

    def _test_create_viewset(self, username):
        for instance in self.instances:
            instance.key += '_new'
            self.assert_create_viewset(username, data=self.get_instance_as_dict(instance))


class OptionTests(TestModelViewsetMixin, OptionsViewsetTestCase):

    instances = Option.objects.all()
    url_names = {
        'viewset': 'internal-options:option'
    }

    def _test_create_viewset(self, username):
        for instance in self.instances:
            instance.key += '_new'
            self.assert_create_viewset(username, data=self.get_instance_as_dict(instance))


class ConditionTests(TestReadOnlyModelViewsetMixin, OptionsViewsetTestCase):

    instances = Condition.objects.all()
    url_names = {
        'viewset': 'internal-options:condition'
    }


class OptionSetAPITests(TestReadOnlyModelViewsetMixin, OptionsViewsetTestCase):

    instances = OptionSet.objects.all()
    url_names = {
        'viewset': 'api-v1-options:optionset'
    }


class OptionAPITests(TestReadOnlyModelViewsetMixin, OptionsViewsetTestCase):

    instances = Option.objects.all()
    url_names = {
        'viewset': 'api-v1-options:option'
    }
