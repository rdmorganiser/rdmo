import pytest
from django.core.exceptions import ValidationError
from rest_framework.exceptions import \
    ValidationError as RestFameworkValidationError

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
    validator.set_context(OptionSetSerializer())

    validator({
        'locked': False
    })


def test_serializer_create_locked(db):
    validator = OptionSetLockedValidator()
    validator.set_context(OptionSetSerializer())

    validator({
        'locked': True
    })


def test_serializer_update(db):
    optionset = OptionSet.objects.first()

    validator = OptionSetLockedValidator()
    validator.set_context(OptionSetSerializer(instance=optionset))

    validator({})


def test_serializer_update_error(db):
    optionset = OptionSet.objects.first()
    optionset.locked = True
    optionset.save()

    validator = OptionSetLockedValidator()
    validator.set_context(OptionSetSerializer(instance=optionset))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'locked': True
        })


def test_serializer_update_lock(db):
    optionset = OptionSet.objects.first()

    validator = OptionSetLockedValidator()
    validator.set_context(OptionSetSerializer(instance=optionset))

    validator({
        'locked': True
    })


def test_serializer_update_unlock(db):
    optionset = OptionSet.objects.first()
    optionset.locked = True
    optionset.save()

    validator = OptionSetLockedValidator()
    validator.set_context(OptionSetSerializer(instance=optionset))

    validator({
        'locked': False
    })
