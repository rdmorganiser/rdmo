from django.test import TestCase

from apps.core.testing.mixins import (
    TestListViewMixin,
    TestModelAPIViewMixin,
    TestListAPIViewMixin
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
        ('anonymous', None),
    )


class ConditionsTests(TestListViewMixin, ConditionsTestCase):

    url_names = {
        'list': 'conditions'
    }
    status_map = {
        'list': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 302}
    }


class ConditionTests(TestModelAPIViewMixin, ConditionsTestCase):

    instances = Condition.objects.all()

    api_url_name = 'conditions:condition'
    api_status_map = {
        'list': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 403},
        'retrieve': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 403},
        'create': {'editor': 201, 'reviewer': 403, 'user': 403, 'anonymous': 403},
        'update': {'editor': 200, 'reviewer': 403, 'user': 403, 'anonymous': 403},
        'delete': {'editor': 204, 'reviewer': 403, 'user': 403, 'anonymous': 403}
    }

    def prepare_create_instance(self, instance):
        instance.key += '_new'
        return instance


class AttributeTests(TestListAPIViewMixin, ConditionsTestCase):

    instances = Attribute.objects.all()

    api_url_name = 'conditions:attribute'
    api_status_map = {
        'list': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 403}
    }


class RelationTests(TestListAPIViewMixin, ConditionsTestCase):

    api_url_name = 'conditions:relation'
    api_status_map = {
        'list': {'editor': 200, 'reviewer': 200, 'user': 200, 'anonymous': 200}
    }
