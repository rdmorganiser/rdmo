import pytest

from django.core.exceptions import ValidationError

from rest_framework.exceptions import ValidationError as RestFameworkValidationError

from ..models import Attribute
from ..serializers.v1 import AttributeSerializer
from ..validators import AttributeLockedValidator


def test_create(db):
    AttributeLockedValidator()({
        'locked': False
    })


def test_create_locked(db):
    AttributeLockedValidator()({
        'locked': True
    })


def test_create_parent(db):
    AttributeLockedValidator()({
        'locked': False,
        'parent': Attribute.objects.get(uri='http://example.com/terms/domain/individual/single')
    })


def test_create_parent_error(db):
    locked_attribute = Attribute.objects.get(uri='http://example.com/terms/domain/individual/single')
    locked_attribute.locked = True
    locked_attribute.save()

    with pytest.raises(ValidationError):
        AttributeLockedValidator()({
            'locked': False,
            'parent': Attribute.objects.get(uri='http://example.com/terms/domain/individual/single')
        })


def test_update(db):
    attribute = Attribute.objects.get(uri='http://example.com/terms/domain/individual/single/text')

    AttributeLockedValidator(attribute)({
        'locked': False
    })


def test_update_lock(db):
    attribute = Attribute.objects.get(uri='http://example.com/terms/domain/individual/single/text')

    AttributeLockedValidator(attribute)({
        'locked': True
    })


def test_update_unlock(db):
    attribute = Attribute.objects.get(uri='http://example.com/terms/domain/individual/single/text')
    attribute.locked = True
    attribute.save()

    AttributeLockedValidator(attribute)({
        'locked': False
    })


def test_update_error(db):
    attribute = Attribute.objects.get(uri='http://example.com/terms/domain/individual/single/text')
    attribute.locked = True
    attribute.save()

    with pytest.raises(ValidationError):
        AttributeLockedValidator(attribute)({
            'locked': True
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


def test_update_parent(db):
    attribute = Attribute.objects.get(uri='http://example.com/terms/domain/individual/single/text')

    AttributeLockedValidator(attribute)({
        'locked': False,
        'parent': attribute
    })


def test_update_parent_error(db):
    locked_attribute = Attribute.objects.get(uri='http://example.com/terms/domain/individual/single')
    locked_attribute.locked = True
    locked_attribute.save()

    attribute = Attribute.objects.get(uri='http://example.com/terms/domain/individual/single/text')
    with pytest.raises(ValidationError):
        AttributeLockedValidator(attribute)({
            'locked': False
        })


def test_serializer_create(db):
    validator = AttributeLockedValidator()
    serializer = AttributeSerializer()

    validator({
        'locked': False
    }, serializer)


def test_serializer_create_locked(db):
    validator = AttributeLockedValidator()
    serializer = AttributeSerializer()

    validator({
        'locked': True
    }, serializer)


def test_serializer_update(db):
    attribute = Attribute.objects.get(uri='http://example.com/terms/domain/individual/single/text')

    validator = AttributeLockedValidator()
    serializer = AttributeSerializer(instance=attribute)

    validator({
        'locked': False
    }, serializer)


def test_serializer_update_error(db):
    attribute = Attribute.objects.get(uri='http://example.com/terms/domain/individual/single/text')
    attribute.locked = True
    attribute.save()

    validator = AttributeLockedValidator()
    serializer = AttributeSerializer(instance=attribute)

    with pytest.raises(RestFameworkValidationError):
        validator({
            'locked': True
        }, serializer)
