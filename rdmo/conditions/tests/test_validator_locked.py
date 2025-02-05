import pytest

from django.core.exceptions import ValidationError

from rest_framework.exceptions import ValidationError as RestFrameworkValidationError

from ..models import Condition
from ..serializers.v1 import ConditionSerializer
from ..validators import ConditionLockedValidator


def test_create(db):
    ConditionLockedValidator()({
        'locked': False
    })


def test_create_locked(db):
    ConditionLockedValidator()({
        'locked': True
    })


def test_update(db):
    condition = Condition.objects.first()

    ConditionLockedValidator(condition)({
        'locked': False
    })


def test_update_error(db):
    condition = Condition.objects.first()
    condition.locked = True
    condition.save()

    with pytest.raises(ValidationError):
        ConditionLockedValidator(condition)({
            'locked': True
        })


def test_update_lock(db):
    condition = Condition.objects.first()

    ConditionLockedValidator(condition)({
        'locked': True
    })


def test_update_unlock(db):
    condition = Condition.objects.first()
    condition.locked = True
    condition.save()

    ConditionLockedValidator(condition)({
        'locked': False
    })


def test_serializer_create(db):
    validator = ConditionLockedValidator()
    serializer = ConditionSerializer()

    validator({
        'locked': False
    }, serializer)


def test_serializer_create_locked(db):
    validator = ConditionLockedValidator()
    serializer = ConditionSerializer()

    validator({
        'locked': True
    }, serializer)


def test_serializer_update(db):
    condition = Condition.objects.first()

    validator = ConditionLockedValidator()
    serializer = ConditionSerializer(instance=condition)

    validator({}, serializer)


def test_serializer_update_error(db):
    condition = Condition.objects.first()
    condition.locked = True
    condition.save()

    validator = ConditionLockedValidator()
    serializer = ConditionSerializer(instance=condition)

    with pytest.raises(RestFrameworkValidationError):
        validator({
            'locked': True
        }, serializer)


def test_serializer_update_lock(db):
    condition = Condition.objects.first()

    validator = ConditionLockedValidator()
    serializer = ConditionSerializer(instance=condition)

    validator({
        'locked': True
    }, serializer)


def test_serializer_update_unlock(db):
    condition = Condition.objects.first()
    condition.locked = True
    condition.save()

    validator = ConditionLockedValidator()
    serializer = ConditionSerializer(instance=condition)

    validator({
        'locked': False
    }, serializer)
