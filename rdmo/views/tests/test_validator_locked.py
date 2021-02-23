import pytest
from django.core.exceptions import ValidationError
from rest_framework.exceptions import \
    ValidationError as RestFameworkValidationError

from ..models import View
from ..serializers.v1 import ViewSerializer
from ..validators import ViewLockedValidator


def test_create(db):
    ViewLockedValidator()({
        'locked': False
    })


def test_create_locked(db):
    ViewLockedValidator()({
        'locked': True
    })


def test_update(db):
    view = View.objects.first()

    ViewLockedValidator(view)({
        'locked': False
    })


def test_update_error(db):
    view = View.objects.first()
    view.locked = True
    view.save()

    with pytest.raises(ValidationError):
        ViewLockedValidator(view)({
            'locked': True
        })


def test_update_lock(db):
    view = View.objects.first()

    ViewLockedValidator(view)({
        'locked': True
    })


def test_update_unlock(db):
    view = View.objects.first()
    view.locked = True
    view.save()

    ViewLockedValidator(view)({
        'locked': False
    })


def test_serializer_create(db):
    validator = ViewLockedValidator()
    validator.set_context(ViewSerializer())

    validator({
        'locked': False
    })


def test_serializer_create_locked(db):
    validator = ViewLockedValidator()
    validator.set_context(ViewSerializer())

    validator({
        'locked': True
    })


def test_serializer_update(db):
    view = View.objects.first()

    validator = ViewLockedValidator()
    validator.set_context(ViewSerializer(instance=view))

    validator({})


def test_serializer_update_error(db):
    view = View.objects.first()
    view.locked = True
    view.save()

    validator = ViewLockedValidator()
    validator.set_context(ViewSerializer(instance=view))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'locked': True
        })


def test_serializer_update_lock(db):
    view = View.objects.first()

    validator = ViewLockedValidator()
    validator.set_context(ViewSerializer(instance=view))

    validator({
        'locked': True
    })


def test_serializer_update_unlock(db):
    view = View.objects.first()
    view.locked = True
    view.save()

    validator = ViewLockedValidator()
    validator.set_context(ViewSerializer(instance=view))

    validator({
        'locked': False
    })
