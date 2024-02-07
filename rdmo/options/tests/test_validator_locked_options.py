import pytest

from django.core.exceptions import ValidationError

from rest_framework.exceptions import ValidationError as RestFameworkValidationError

from ..models import Option, OptionSet
from ..serializers.v1 import OptionSerializer
from ..validators import OptionLockedValidator


def test_create(db):
    OptionLockedValidator()({
        'locked': False
    })


def test_create_locked(db):
    OptionLockedValidator()({
        'locked': True
    })


def test_create_optionset(db):
    optionset = OptionSet.objects.first()

    OptionLockedValidator()({
        'optionsets': [optionset],
        'locked': False
    })


def test_create_optionset_error(db):
    optionset = OptionSet.objects.first()
    optionset.locked = True
    optionset.save()

    with pytest.raises(ValidationError):
        OptionLockedValidator()({
            'optionsets': [optionset],
            'locked': False
        })


def test_update(db):
    option = Option.objects.first()

    OptionLockedValidator(option)({
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


def test_update_error(db):
    option = Option.objects.first()
    option.locked = True
    option.save()

    with pytest.raises(ValidationError):
        OptionLockedValidator(option)({
            'locked': True
        })


def test_update_optionset(db):
    optionset = OptionSet.objects.first()

    option = Option.objects.exclude(optionsets=optionset).first()
    OptionLockedValidator(option)({
        'optionsets': [optionset],
        'locked': False
    })


def test_update_optionset_error(db):
    optionset = OptionSet.objects.first()
    optionset.locked = True
    optionset.save()

    option = Option.objects.exclude(optionsets=optionset).first()
    with pytest.raises(ValidationError):
        OptionLockedValidator(option)({
            'optionsets': [optionset],
            'locked': False
        })


def test_serializer_create(db):
    validator = OptionLockedValidator()
    serializer = OptionSerializer()

    validator({
        'locked': False
    }, serializer)


def test_serializer_create_locked(db):
    validator = OptionLockedValidator()
    serializer = OptionSerializer()

    validator({
        'locked': True
    }, serializer)


def test_serializer_update(db):
    option = Option.objects.first()

    validator = OptionLockedValidator()
    serializer = OptionSerializer(instance=option)

    validator({
        'locked': False
    }, serializer)


def test_serializer_update_error(db):
    option = Option.objects.first()
    option.locked = True
    option.save()

    validator = OptionLockedValidator()
    serializer = OptionSerializer(instance=option)

    with pytest.raises(RestFameworkValidationError):
        validator({
            'locked': True
        }, serializer)
