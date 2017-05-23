from django.test import TestCase

from test_mixins.views import TestListViewMixin
from test_mixins.viewsets import (
    TestModelViewsetMixin,
    TestListViewsetMixin,
    TestRetrieveViewsetMixin,
    TestUpdateViewsetMixin,
    TestDeleteViewsetMixin
)

from apps.core.testing.mixins import TestExportViewMixin, TestImportViewMixin
from apps.accounts.utils import set_group_permissions

from apps.conditions.models import Condition
from apps.options.models import OptionSet

from .models import AttributeEntity, Attribute, Range, VerboseName


class DomainTestCase(TestCase):

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


class DomainTests(TestListViewMixin, DomainTestCase):

    url_names = {
        'list_view': 'domain'
    }


class AttributeEntityTests(TestModelViewsetMixin, DomainTestCase):

    # get entities and order them by level to delete the entities at the bottom of the tree first
    instances = AttributeEntity.objects.filter(attribute=None).order_by('-level')
    url_names = {
        'viewset': 'internal-domain:entity'
    }
    restore_instance = False

    def prepare_create_instance(self, instance):
        instance.key += '_new'
        return instance


class AttributeTests(TestModelViewsetMixin, DomainTestCase):

    instances = Attribute.objects.all()
    url_names = {
        'viewset': 'internal-domain:attribute'
    }

    def prepare_create_instance(self, instance):
        instance.key += '_new'
        return instance


class RangeTests(TestListViewsetMixin, TestRetrieveViewsetMixin, TestUpdateViewsetMixin, TestDeleteViewsetMixin, DomainTestCase):

    instances = Range.objects.all()
    url_names = {
        'viewset': 'internal-domain:range'
    }


class VerboseNameTests(TestListViewsetMixin, TestRetrieveViewsetMixin, TestUpdateViewsetMixin, TestDeleteViewsetMixin, DomainTestCase):

    instances = VerboseName.objects.all()
    url_names = {
        'viewset': 'internal-domain:verbosename'
    }


class ValueTypeTests(TestListViewsetMixin, DomainTestCase):

    url_names = {
        'viewset': 'internal-domain:valuestype'
    }
    status_map = {
        'list_viewset': {
            'editor': 200, 'reviewer': 200, 'reviewer': 200, 'api': 200, 'user': 200, 'anonymous': 403
        }
    }


class OptionSetTests(TestListViewsetMixin, TestRetrieveViewsetMixin, DomainTestCase):

    instances = OptionSet.objects.all()
    url_names = {
        'viewset': 'internal-domain:optionset'
    }


class ConditionTests(TestListViewsetMixin, TestRetrieveViewsetMixin, DomainTestCase):

    instances = Condition.objects.all()
    url_names = {
        'viewset': 'internal-domain:condition'
    }


class DomainExportTests(TestExportViewMixin, DomainTestCase):

    url_names = {
        'list_view': 'domain',
        'export_view': 'domain_export'
    }
    export_formats = ('xml', 'html', 'rtf', 'csv')


class DomainImportTests(TestImportViewMixin, TestCase):

    import_file = 'testing/xml/domain.xml'


class AttributeEntityAPITests(TestListViewsetMixin, TestRetrieveViewsetMixin, DomainTestCase):

    instances = AttributeEntity.objects.filter(attribute=None)
    url_names = {
        'viewset': 'api-v1-domain:entity'
    }


class AttributeAPITests(TestListViewsetMixin, TestRetrieveViewsetMixin, DomainTestCase):

    instances = Attribute.objects.all()
    url_names = {
        'viewset': 'api-v1-domain:attribute'
    }
