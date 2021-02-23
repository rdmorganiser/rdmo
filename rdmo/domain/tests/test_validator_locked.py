import pytest
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework.exceptions import \
    ValidationError as RestFameworkValidationError

from ..models import Attribute
from ..serializers.v1 import AttributeSerializer
from ..validators import AttributeLockedValidator


def test_create(db):
    AttributeLockedValidator()({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'key': 'test',
        'parent': Attribute.objects.get(uri='http://example.com/terms/domain/individual/single')
    })


def test_create_no_parent(db):
    AttributeLockedValidator()({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'key': 'test'
    })


def test_create_error(db):
    locked_attribute = Attribute.objects.get(uri='http://example.com/terms/domain/individual/single')
    locked_attribute.locked = True
    locked_attribute.save()

    with pytest.raises(ValidationError):
        AttributeLockedValidator()({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'key': 'test',
            'parent': Attribute.objects.get(uri='http://example.com/terms/domain/individual/single')
        })


def test_update(db):
    attribute = Attribute.objects.get(uri='http://example.com/terms/domain/individual/single/text')

    AttributeLockedValidator(attribute)({
        'uri_prefix': attribute.uri_prefix,
        'key': attribute.key,
        'parent': attribute.parent
    })


def test_update_error(db):
    attribute = Attribute.objects.get(uri='http://example.com/terms/domain/individual/single/text')
    attribute.locked = True
    attribute.save()

    with pytest.raises(ValidationError):
        AttributeLockedValidator(attribute)({
            'uri_prefix': attribute.uri_prefix,
            'key': attribute.key,
            'parent': attribute.parent,
            'locked': True
        })


def test_update_lock(db):
    attribute = Attribute.objects.get(uri='http://example.com/terms/domain/individual/single/text')

    AttributeLockedValidator(attribute)({
        'uri_prefix': attribute.uri_prefix,
        'key': attribute.key,
        'parent':  attribute.parent,
        'locked': True
    })


def test_update_unlock(db):
    attribute = Attribute.objects.get(uri='http://example.com/terms/domain/individual/single/text')
    attribute.locked = True
    attribute.save()

    AttributeLockedValidator(attribute)({
        'uri_prefix': attribute.uri_prefix,
        'key': attribute.key,
        'parent':  attribute.parent,
        'locked': False
    })


def test_update_error_parent(db):
    locked_attribute = Attribute.objects.get(uri='http://example.com/terms/domain/individual/single')
    locked_attribute.locked = True
    locked_attribute.save()

    attribute = Attribute.objects.get(uri='http://example.com/terms/domain/individual/single/text')
    with pytest.raises(ValidationError):
        AttributeLockedValidator(attribute)({
            'uri_prefix': attribute.uri_prefix,
            'key': attribute.key,
            'parent': attribute.parent
        })


def test_serializer_create(db):
    validator = AttributeLockedValidator()
    validator.set_context(AttributeSerializer())

    validator({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'key': 'test',
        'parent': Attribute.objects.get(uri='http://example.com/terms/domain/individual/single')
    })


def test_serializer_create_no_parent(db):
    validator = AttributeLockedValidator()
    validator.set_context(AttributeSerializer())

    validator({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'key': 'test'
    })


def test_serializer_create_error(db):
    locked_attribute = Attribute.objects.get(uri='http://example.com/terms/domain/individual/single')
    locked_attribute.locked = True
    locked_attribute.save()

    validator = AttributeLockedValidator()
    validator.set_context(AttributeSerializer())

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'key': 'test',
            'parent': locked_attribute
        })


def test_serializer_update(db):
    attribute = Attribute.objects.get(uri='http://example.com/terms/domain/individual/single/text')

    validator = AttributeLockedValidator()
    validator.set_context(AttributeSerializer(instance=attribute))

    validator({
        'uri_prefix': attribute.uri_prefix,
        'key': attribute.key,
        'parent':  attribute.parent
    })


def test_serializer_update_error(db):
    attribute = Attribute.objects.get(uri='http://example.com/terms/domain/individual/single/text')
    attribute.locked = True
    attribute.save()

    validator = AttributeLockedValidator()
    validator.set_context(AttributeSerializer(instance=attribute))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': attribute.uri_prefix,
            'key': attribute.key,
            'parent':  attribute.parent,
            'locked': True
        })


def test_serializer_update_lock(db):
    attribute = Attribute.objects.get(uri='http://example.com/terms/domain/individual/single/text')

    validator = AttributeLockedValidator()
    validator.set_context(AttributeSerializer(instance=attribute))

    validator({
        'uri_prefix': attribute.uri_prefix,
        'key': attribute.key,
        'parent':  attribute.parent,
        'locked': True
    })


def test_serializer_update_unlock(db):
    attribute = Attribute.objects.get(uri='http://example.com/terms/domain/individual/single/text')
    attribute.locked = True
    attribute.save()

    validator = AttributeLockedValidator()
    validator.set_context(AttributeSerializer(instance=attribute))

    validator({
        'uri_prefix': attribute.uri_prefix,
        'key': attribute.key,
        'parent':  attribute.parent,
        'locked': False
    })


def test_serializer_update_error_parent(db):
    locked_attribute = Attribute.objects.get(uri='http://example.com/terms/domain/individual/single')
    locked_attribute.locked = True
    locked_attribute.save()

    attribute = Attribute.objects.get(uri='http://example.com/terms/domain/individual/single/text')

    validator = AttributeLockedValidator()
    validator.set_context(AttributeSerializer(instance=attribute))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': attribute.uri_prefix,
            'key': attribute.key,
            'parent':  attribute.parent
        })
