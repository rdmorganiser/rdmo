import pytest
from django.core.exceptions import ValidationError
from rest_framework.exceptions import \
    ValidationError as RestFameworkValidationError

from ..models import Option, OptionSet
from ..serializers.v1 import OptionSerializer
from ..validators import OptionLockedValidator


def test_create(db):
    OptionLockedValidator()({
        'optionsets': [OptionSet.objects.first()],
        'locked': False
    })


def test_create_locked(db):
    OptionLockedValidator()({
        'optionsets': [OptionSet.objects.first()],
        'locked': True
    })


def test_update(db):
    option = Option.objects.first()

    OptionLockedValidator(option)({
        'optionsets': option.optionsets.all(),
        'locked': False
    })


def test_update_error(db):
    option = Option.objects.first()
    option.locked = True
    option.save()

    with pytest.raises(ValidationError):
        OptionLockedValidator(option)({
            'optionsets': option.optionsets.all(),
            'locked': True
        })


def test_update_parent_error(db):
    option = Option.objects.first()
    optionset = option.optionsets.first()
    optionset.locked = True
    optionset.save()

    with pytest.raises(ValidationError):
        OptionLockedValidator(option)({
            'optionsets': [optionset],
            'locked': False
        })


def test_update_different_parent_error(db):
    option = Option.objects.first()
    optionset = OptionSet.objects.exclude(pk__in=[optionset.pk for optionset in option.optionsets.all()]).first()
    optionset.locked = True
    optionset.save()

    with pytest.raises(ValidationError):
        OptionLockedValidator(option)({
            'optionsets': [optionset],
            'locked': False
        })


def test_update_lock(db):
    option = Option.objects.first()

    OptionLockedValidator(option)({
        'optionsets': option.optionsets.all(),
        'locked': True
    })


def test_update_unlock(db):
    option = Option.objects.first()
    option.locked = True
    option.save()

    OptionLockedValidator(option)({
        'optionsets': option.optionsets.all(),
        'locked': False
    })


def test_serializer_create(db):
    validator = OptionLockedValidator()
    validator.set_context(OptionSerializer())

    validator({
        'optionsets': [OptionSet.objects.first()],
        'locked': False
    })


def test_serializer_create_locked(db):
    validator = OptionLockedValidator()
    validator.set_context(OptionSerializer())

    validator({
        'optionsets': [OptionSet.objects.first()],
        'locked': True
    })


def test_serializer_update(db):
    option = Option.objects.first()

    validator = OptionLockedValidator()
    validator.set_context(OptionSerializer(instance=option))

    validator({
        'optionsets': option.optionsets.all(),
        'locked': False
    })


def test_serializer_update_error(db):
    option = Option.objects.first()
    option.locked = True
    option.save()

    validator = OptionLockedValidator()
    validator.set_context(OptionSerializer(instance=option))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'optionsets': option.optionsets.all(),
            'locked': True
        })


def test_serializer_update_parent_error(db):
    option = Option.objects.first()
    optionset = option.optionsets.first()
    optionset.locked = True
    optionset.save()

    validator = OptionLockedValidator()
    validator.set_context(OptionSerializer(instance=option))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'optionsets': [optionset],
            'locked': False
        })


def test_serializer_update_different_parent_error(db):
    option = Option.objects.first()
    optionset = OptionSet.objects.exclude(pk__in=[optionset.pk for optionset in option.optionsets.all()]).first()
    optionset.locked = True
    optionset.save()

    validator = OptionLockedValidator()
    validator.set_context(OptionSerializer(instance=option))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'optionsets': [optionset],
            'locked': False
        })


def test_serializer_update_lock(db):
    option = Option.objects.first()

    validator = OptionLockedValidator()
    validator.set_context(OptionSerializer(instance=option))

    validator({
        'optionsets': option.optionsets.all(),
        'locked': True
    })


def test_serializer_update_unlock(db):
    option = Option.objects.first()
    option.locked = True
    option.save()

    validator = OptionLockedValidator()
    validator.set_context(OptionSerializer(instance=option))

    validator({
        'optionsets': option.optionsets.all(),
        'locked': False
    })
