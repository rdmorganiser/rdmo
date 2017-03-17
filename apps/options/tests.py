from django.test import TestCase

from apps.core.testing.mixins import (
    TestListViewMixin,
    TestExportListViewMixin,
    TestModelAPIViewMixin,
    TestListAPIViewMixin,
    TestRetrieveAPIViewMixin
)

from apps.conditions.models import Condition

from .models import OptionSet, Option


class OptionsTestCase(TestCase):

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


class OptionsTests(TestListViewMixin, TestExportListViewMixin, OptionsTestCase):

    url_names = {
        'list': 'options',
        'export': 'options_export'
    }
    status_map = {
        'list': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 302},
        'export': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 302}
    }


class OptionSetTests(TestModelAPIViewMixin, OptionsTestCase):

    instances = OptionSet.objects.all()

    api_url_name = 'options:optionset'
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


class OptionTests(TestModelAPIViewMixin, OptionsTestCase):

    instances = Option.objects.all()

    api_url_name = 'options:option'
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


class ConditionTests(TestListAPIViewMixin, TestRetrieveAPIViewMixin, OptionsTestCase):

    instances = Condition.objects.all()

    api_url_name = 'options:condition'
    api_status_map = {
        'list': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 403},
        'retrieve': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 403},
    }
