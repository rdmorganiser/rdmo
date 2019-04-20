from django.test import TestCase

from test_generator.viewsets import TestModelViewsetMixin

from rdmo.core.testing.mixins import TestTranslationMixin

from rdmo.accounts.utils import set_group_permissions

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
            'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 401
        },
        'detail_viewset': {
            'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 401
        },
        'create_viewset': {
            'editor': 201, 'reviewer': 403, 'api': 201, 'user': 403, 'anonymous': 401
        },
        'update_viewset': {
            'editor': 200, 'reviewer': 403, 'api': 200, 'user': 403, 'anonymous': 401
        },
        'delete_viewset': {
            'editor': 204, 'reviewer': 403, 'api': 204, 'user': 403, 'anonymous': 401
        }
    }

    @classmethod
    def setUpTestData(cls):
        set_group_permissions()


class OptionSetTests(TestModelViewsetMixin, OptionsViewsetTestCase):

    instances = OptionSet.objects.all()
    url_names = {
        'viewset': 'v1-options:optionset'
    }

    def _test_create_viewset(self, username):
        for instance in self.instances:
            instance.key += '_new'
            self.assert_create_viewset(username, data=self.get_instance_as_dict(instance))


class OptionTests(TestTranslationMixin, TestModelViewsetMixin, OptionsViewsetTestCase):

    instances = Option.objects.all()
    url_names = {
        'viewset': 'v1-options:option'
    }
    trans_fields = ('text', )

    def _test_create_viewset(self, username):
        for instance in self.instances:
            instance.key += '_new'
            self.assert_create_viewset(username, data=self.get_instance_as_dict(instance))
