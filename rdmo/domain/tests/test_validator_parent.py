import pytest

from django.conf import settings
from django.core.exceptions import ValidationError

from rest_framework.exceptions import ValidationError as RestFameworkValidationError

from ..models import Attribute
from ..serializers.v1 import AttributeSerializer
from ..validators import AttributeParentValidator


def test_create(db):
    AttributeParentValidator()({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'key': 'test',
        'parent': Attribute.objects.get(uri='http://example.com/terms/domain/individual/single')
    })


def test_update(db):
    attribute = Attribute.objects.get(uri='http://example.com/terms/domain/individual/single/text')
    AttributeParentValidator(attribute)({
        'uri_prefix': attribute.uri_prefix,
        'key': attribute.key,
        'parent': attribute.parent
    })


def test_update_error(db):
    attribute = Attribute.objects.get(uri='http://example.com/terms/domain/individual/single/text')
    with pytest.raises(ValidationError):
        AttributeParentValidator(attribute)({
            'uri_prefix': attribute.uri_prefix,
            'key': attribute.key,
            'parent': attribute  # set self as parent
        })


def test_serializer_create(db):
    class MockedView:
        action = 'create'

    validator = AttributeParentValidator()
    serializer = AttributeSerializer()
    serializer.context['view'] = MockedView()

    validator({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'key': 'test',
        'parent': Attribute.objects.get(uri='http://example.com/terms/domain/individual/single')
    }, serializer)


def test_serializer_update(db):
    attribute = Attribute.objects.get(uri='http://example.com/terms/domain/individual/single/text')
    validator = AttributeParentValidator()
    serializer = AttributeSerializer(instance=attribute)

    validator({
        'uri_prefix': attribute.uri_prefix,
        'key': attribute.key,
        'parent':  attribute.parent
    }, serializer)


def test_serializer_update_error(db):
    attribute = Attribute.objects.get(uri='http://example.com/terms/domain/individual/single/text')
    validator = AttributeParentValidator()
    serializer = AttributeSerializer(instance=attribute)

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': attribute.uri_prefix,
            'key': attribute.key,
            'parent':  attribute  # set self as parent
        }, serializer)


def test_import_create(db):
    AttributeParentValidator()({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'key': 'test',
        'parent_id': Attribute.objects.get(uri='http://example.com/terms/domain/individual/single').id
    })


def test_import_update(db):
    attribute = Attribute.objects.get(uri='http://example.com/terms/domain/individual/single/text')
    AttributeParentValidator(attribute)({
        'uri_prefix': attribute.uri_prefix,
        'key': attribute.key,
        'parent_id': attribute.parent.id
    })


def test_import_update_error(db):
    attribute = Attribute.objects.get(uri='http://example.com/terms/domain/individual/single/text')
    with pytest.raises(ValidationError):
        AttributeParentValidator(attribute)({
            'uri_prefix': attribute.uri_prefix,
            'key': attribute.key,
            'parent_id': attribute.id  # set self as parent
        })
