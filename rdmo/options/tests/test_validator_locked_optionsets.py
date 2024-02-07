import pytest

from django.core.exceptions import ValidationError

from rest_framework.exceptions import ValidationError as RestFameworkValidationError

from ..models import OptionSet
from ..serializers.v1 import OptionSetSerializer
from ..validators import OptionSetLockedValidator


def test_create(db):
    OptionSetLockedValidator()({
        'locked': False
    })


def test_create_locked(db):
    OptionSetLockedValidator()({
        'locked': True
    })


def test_update(db):
    optionset = OptionSet.objects.first()

    OptionSetLockedValidator(optionset)({
        'locked': False
    })


def test_update_error(db):
    optionset = OptionSet.objects.first()
    optionset.locked = True
    optionset.save()

    with pytest.raises(ValidationError):
        OptionSetLockedValidator(optionset)({
            'locked': True
        })


def test_update_lock(db):
    optionset = OptionSet.objects.first()

    OptionSetLockedValidator(optionset)({
        'locked': True
    })


def test_update_unlock(db):
    optionset = OptionSet.objects.first()
    optionset.locked = True
    optionset.save()

    OptionSetLockedValidator(optionset)({
        'locked': False
    })


def test_serializer_create(db):
    validator = OptionSetLockedValidator()
    serializer = OptionSetSerializer()

    validator({
        'locked': False
    }, serializer)


def test_serializer_create_locked(db):
    validator = OptionSetLockedValidator()
    serializer = OptionSetSerializer()

    validator({
        'locked': True
    }, serializer)


def test_serializer_update(db):
    optionset = OptionSet.objects.first()

    validator = OptionSetLockedValidator()
    serializer = OptionSetSerializer(instance=optionset)

    validator({
        'locked': False
    }, serializer)


def test_serializer_update_error(db):
    optionset = OptionSet.objects.first()
    optionset.locked = True
    optionset.save()

    validator = OptionSetLockedValidator()
    serializer = OptionSetSerializer(instance=optionset)

    with pytest.raises(RestFameworkValidationError):
        validator({
            'locked': True
        }, serializer)
