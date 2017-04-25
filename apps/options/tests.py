from django.test import TestCase

from apps.core.testing.mixins import (
    TestListViewMixin,
    TestExportViewMixin,
    TestImportViewMixin,
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


class OptionsTests(TestListViewMixin, OptionsTestCase):

    url_names = {
        'list': 'options'
    }


class OptionSetTests(TestModelAPIViewMixin, OptionsTestCase):

    instances = OptionSet.objects.all()

    api_url_name = 'internal-options:optionset'

    def prepare_create_instance(self, instance):
        instance.key += '_new'
        return instance


class OptionTests(TestModelAPIViewMixin, OptionsTestCase):

    instances = Option.objects.all()

    api_url_name = 'internal-options:option'

    def prepare_create_instance(self, instance):
        instance.key += '_new'
        return instance


class ConditionTests(TestListAPIViewMixin, TestRetrieveAPIViewMixin, OptionsTestCase):

    instances = Condition.objects.all()

    api_url_name = 'internal-options:condition'


class OptionsExportTests(TestExportViewMixin, OptionsTestCase):

    url_names = {
        'export': 'options_export'
    }


class OptionsImportTests(TestImportViewMixin, TestCase):

    import_file = 'testing/xml/options.xml'


class OptionSetAPITests(TestListAPIViewMixin, TestRetrieveAPIViewMixin, OptionsTestCase):

    instances = OptionSet.objects.all()

    api_url_name = 'api-v1-options:optionset'


class OptionAPITests(TestListAPIViewMixin, TestRetrieveAPIViewMixin, OptionsTestCase):

    instances = Option.objects.all()

    api_url_name = 'api-v1-options:option'
