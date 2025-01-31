import pytest

from django.conf import settings
from django.core.exceptions import ValidationError

from rest_framework.exceptions import ValidationError as RestFrameworkValidationError

from ..models import Attribute
from ..serializers.v1 import AttributeSerializer
from ..validators import AttributeUniqueURIValidator


def test_validator_create(db):
    AttributeUniqueURIValidator()({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'key': 'test',
        'parent': Attribute.objects.get(uri='http://example.com/terms/domain/individual/single')
    })


def test_validator_create_error(db):
    with pytest.raises(ValidationError):
        AttributeUniqueURIValidator()({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'key': 'text',
            'parent': Attribute.objects.get(uri='http://example.com/terms/domain/individual/single')
        })


def test_validator_update(db):
    attribute = Attribute.objects.get(uri='http://example.com/terms/domain/individual/single/text')
    AttributeUniqueURIValidator(attribute)({
        'uri_prefix': attribute.uri_prefix,
        'key': attribute.key,
        'parent': attribute.parent
    })


def test_validator_update_error(db):
    attribute = Attribute.objects.get(uri='http://example.com/terms/domain/individual/single/text')

    with pytest.raises(ValidationError):
        AttributeUniqueURIValidator(attribute)({
            'uri_prefix': attribute.uri_prefix,
            'key': 'textarea',
            'parent': attribute.parent
        })


def test_validator_serializer_create(db):
    validator = AttributeUniqueURIValidator()
    serializer = AttributeSerializer()

    validator({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'key': 'test',
        'parent': Attribute.objects.get(uri='http://example.com/terms/domain/individual/single')
    }, serializer)


def test_validator_serializer_create_error(db):
    validator = AttributeUniqueURIValidator()
    serializer = AttributeSerializer()

    with pytest.raises(RestFrameworkValidationError):
        validator({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'key': 'text',
            'parent': Attribute.objects.get(uri='http://example.com/terms/domain/individual/single')
        }, serializer)


def test_validator_serializer_update(db):
    attribute = Attribute.objects.get(uri='http://example.com/terms/domain/individual/single/text')
    validator = AttributeUniqueURIValidator()
    serializer = AttributeSerializer(instance=attribute)

    validator({
        'uri_prefix': attribute.uri_prefix,
        'key': 'test',
        'parent':  attribute.parent
    }, serializer)


def test_validator_serializer_update_error(db):
    attribute = Attribute.objects.get(uri='http://example.com/terms/domain/individual/single/text')
    validator = AttributeUniqueURIValidator()
    serializer = AttributeSerializer(instance=attribute)

    with pytest.raises(RestFrameworkValidationError):
        validator({
            'uri_prefix': attribute.uri_prefix,
            'key': 'textarea',
            'parent': attribute.parent
        }, serializer)
