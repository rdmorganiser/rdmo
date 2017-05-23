from django.test import TestCase

from test_mixins.views import TestListViewMixin
from test_mixins.viewsets import TestModelViewsetMixin, TestListViewsetMixin, TestRetrieveViewsetMixin

from apps.core.testing.mixins import TestExportViewMixin, TestImportViewMixin
from apps.accounts.utils import set_group_permissions

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

    def setUp(self):
        set_group_permissions()


class OptionsTests(TestListViewMixin, OptionsTestCase):

    url_names = {
        'list_view': 'options'
    }


class OptionSetTests(TestModelViewsetMixin, OptionsTestCase):

    instances = OptionSet.objects.all()
    url_names = {
        'viewset': 'internal-options:optionset'
    }

    def prepare_create_instance(self, instance):
        instance.key += '_new'
        return instance


class OptionTests(TestModelViewsetMixin, OptionsTestCase):

    instances = Option.objects.all()
    url_names = {
        'viewset': 'internal-options:option'
    }

    def prepare_create_instance(self, instance):
        instance.key += '_new'
        return instance


class ConditionTests(TestListViewsetMixin, TestRetrieveViewsetMixin, OptionsTestCase):

    instances = Condition.objects.all()
    url_names = {
        'viewset': 'internal-options:condition'
    }


class OptionsExportTests(TestExportViewMixin, OptionsTestCase):

    url_names = {
        'export_view': 'options_export'
    }


class OptionsImportTests(TestImportViewMixin, TestCase):

    import_file = 'testing/xml/options.xml'


class OptionSetAPITests(TestListViewsetMixin, TestRetrieveViewsetMixin, OptionsTestCase):

    instances = OptionSet.objects.all()
    url_names = {
        'viewset': 'api-v1-options:optionset'
    }


class OptionAPITests(TestListViewsetMixin, TestRetrieveViewsetMixin, OptionsTestCase):

    instances = Option.objects.all()
    url_names = {
        'viewset': 'api-v1-options:option'
    }
