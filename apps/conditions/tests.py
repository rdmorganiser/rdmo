from django.test import TestCase

from apps.core.testing.mixins import (
    TestListViewMixin,
    TestExportViewMixin,
    TestImportViewMixin,
    TestModelAPIViewMixin,
    TestListAPIViewMixin,
    TestRetrieveAPIViewMixin
)

from apps.domain.models import Attribute

from .models import Condition


class ConditionsTestCase(TestCase):

    lang = 'en'

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
        'list': {'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 302},
        'export': {'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 302}
    }

    api_status_map = {
        'list': {'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 403},
        'retrieve': {'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 403},
        'create': {'editor': 201, 'reviewer': 403, 'api': 403, 'user': 403, 'anonymous': 403},
        'update': {'editor': 200, 'reviewer': 403, 'api': 403, 'user': 403, 'anonymous': 403},
        'delete': {'editor': 204, 'reviewer': 403, 'api': 403, 'user': 403, 'anonymous': 403}
    }


class ConditionsTests(TestListViewMixin, ConditionsTestCase):

    url_names = {
        'list': 'conditions'
    }


class ConditionTests(TestModelAPIViewMixin, ConditionsTestCase):

    instances = Condition.objects.all()

    api_url_name = 'internal-conditions:condition'

    def prepare_create_instance(self, instance):
        instance.key += '_new'
        return instance


class AttributeTests(TestListAPIViewMixin, ConditionsTestCase):

    instances = Attribute.objects.all()

    api_url_name = 'internal-conditions:attribute'


class RelationTests(TestListAPIViewMixin, ConditionsTestCase):

    api_url_name = 'internal-conditions:relation'
    api_status_map = {
        'list': {'editor': 200, 'reviewer': 200, 'api': 200, 'user': 200, 'anonymous': 403}
    }


class ConditionExportTests(TestExportViewMixin, ConditionsTestCase):

    url_names = {
        'export': 'conditions_export'
    }


class ConditionImportTests(TestImportViewMixin, TestCase):

    import_file = 'testing/xml/conditions.xml'


class ConditionAPITests(TestListAPIViewMixin, TestRetrieveAPIViewMixin, ConditionsTestCase):

    instances = Condition.objects.all()

    api_url_name = 'api-v1-conditions:condition'
