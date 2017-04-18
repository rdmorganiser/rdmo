from django.test import TestCase

from apps.core.testing.mixins import (
    TestListViewMixin,
    TestExportViewMixin,
    TestImportViewMixin,
    TestModelAPIViewMixin,
    TestListAPIViewMixin,
    TestRetrieveAPIViewMixin,
    TestUpdateAPIViewMixin,
    TestDeleteAPIViewMixin
)

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
        ('anonymous', None),
    )


class DomainTests(TestListViewMixin, DomainTestCase):

    url_names = {
        'list': 'domain'
    }
    status_map = {
        'list': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 302}
    }


class AttributeEntityTests(TestModelAPIViewMixin, DomainTestCase):

    # get entities and order them by level to delete the entities at the bottom of the tree first
    instances = AttributeEntity.objects.filter(attribute=None).order_by('-level')

    api_url_name = 'internal-domain:entity'
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


class AttributeTests(TestModelAPIViewMixin, DomainTestCase):

    instances = Attribute.objects.all()

    api_url_name = 'internal-domain:attribute'
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


class RangeTests(TestListAPIViewMixin, TestRetrieveAPIViewMixin, TestUpdateAPIViewMixin, TestDeleteAPIViewMixin, DomainTestCase):

    instances = Range.objects.all()

    api_url_name = 'internal-domain:range'
    api_status_map = {
        'list': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 403},
        'retrieve': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 403},
        'update': {'editor': 200, 'reviewer': 403, 'user': 403, 'anonymous': 403},
        'delete': {'editor': 204, 'reviewer': 403, 'user': 403, 'anonymous': 403}
    }


class VerboseNameTests(TestListAPIViewMixin, TestRetrieveAPIViewMixin, TestUpdateAPIViewMixin, TestDeleteAPIViewMixin, DomainTestCase):

    instances = VerboseName.objects.all()

    api_url_name = 'internal-domain:verbosename'
    api_status_map = {
        'list': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 403},
        'retrieve': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 403},
        'update': {'editor': 200, 'reviewer': 403, 'user': 403, 'anonymous': 403},
        'delete': {'editor': 204, 'reviewer': 403, 'user': 403, 'anonymous': 403}
    }


class ValueTypeTests(TestListAPIViewMixin, DomainTestCase):

    api_url_name = 'internal-domain:valuestype'
    api_status_map = {
        'list': {'editor': 200, 'reviewer': 200, 'user': 200, 'anonymous': 200}
    }


class OptionSetTests(TestListAPIViewMixin, TestRetrieveAPIViewMixin, DomainTestCase):

    instances = OptionSet.objects.all()

    api_url_name = 'internal-domain:optionset'
    api_status_map = {
        'list': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 403},
        'retrieve': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 403}
    }


class ConditionTests(TestListAPIViewMixin, TestRetrieveAPIViewMixin, DomainTestCase):

    instances = Condition.objects.all()

    api_url_name = 'internal-domain:condition'
    api_status_map = {
        'list': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 403},
        'retrieve': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 403}
    }


class DomainExportTests(TestExportViewMixin, DomainTestCase):

    url_names = {
        'list': 'domain',
        'export': 'domain_export'
    }
    status_map = {
        'list': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 302},
        'export': {'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 302}
    }
    export_formats = ('xml', 'html', 'rtf', 'csv')


class DomainImportTests(TestImportViewMixin, TestCase):

    import_file = 'testing/xml/domain.xml'
