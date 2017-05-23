from django.test import TestCase

from test_mixins.views import TestListViewMixin
from test_mixins.viewsets import TestModelViewsetMixin, TestListViewsetMixin, TestRetrieveViewsetMixin

from apps.core.testing.mixins import TestExportViewMixin, TestImportViewMixin
from apps.accounts.utils import set_group_permissions
from apps.domain.models import Attribute

from .models import Condition


class ConditionsTestCase(TestCase):

    fixtures = (
        'users.json',
        'groups.json',
        'accounts.json',
        'conditions.json',
        'domain.json',
        'options.json',
    )

    languages = (
        'en',
    )

    users = (
        ('editor', 'editor'),
        ('reviewer', 'reviewer'),
        ('user', 'user'),
        ('api', 'api'),
        ('anonymous', None),
    )

    status_map = {
        'list_view': {
            'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 302
        },
        'export_view': {
            'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 302
        },
        'list_viewset': {
            'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 403
        },
        'retrieve_viewset': {
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


class ConditionsTests(TestListViewMixin, ConditionsTestCase):

    url_names = {
        'list_view': 'conditions'
    }


class ConditionTests(TestModelViewsetMixin, ConditionsTestCase):

    instances = Condition.objects.all()
    url_names = {
        'viewset': 'internal-conditions:condition'
    }

    def prepare_create_instance(self, instance):
        instance.key += '_new'
        return instance


class AttributeTests(TestListViewsetMixin, ConditionsTestCase):

    instances = Attribute.objects.all()
    url_names = {
        'viewset': 'internal-conditions:attribute'
    }


class RelationTests(TestListViewsetMixin, ConditionsTestCase):

    url_names = {
        'viewset': 'internal-conditions:relation'
    }
    status_map = {
        'list_viewset': {'editor': 200, 'reviewer': 200, 'api': 200, 'user': 200, 'anonymous': 403}
    }


class ConditionExportTests(TestExportViewMixin, ConditionsTestCase):

    url_names = {
        'export_view': 'conditions_export'
    }


class ConditionImportTests(TestImportViewMixin, TestCase):

    import_file = 'testing/xml/conditions.xml'


class ConditionAPITests(TestListViewsetMixin, TestRetrieveViewsetMixin, ConditionsTestCase):

    instances = Condition.objects.all()
    url_names = {
        'viewset': 'api-v1-conditions:condition'
    }
