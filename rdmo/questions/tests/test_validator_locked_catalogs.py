import pytest
from django.core.exceptions import ValidationError
from rest_framework.exceptions import \
    ValidationError as RestFameworkValidationError

from ..models import Catalog
from ..serializers.v1 import CatalogSerializer
from ..validators import CatalogLockedValidator


def test_create(db):
    CatalogLockedValidator()({
        'locked': False
    })


def test_create_locked(db):
    CatalogLockedValidator()({
        'locked': True
    })


def test_update(db):
    catalog = Catalog.objects.first()

    CatalogLockedValidator(catalog)({
        'locked': False
    })


def test_update_error(db):
    catalog = Catalog.objects.first()
    catalog.locked = True
    catalog.save()

    with pytest.raises(ValidationError):
        CatalogLockedValidator(catalog)({
            'locked': True
        })


def test_update_lock(db):
    catalog = Catalog.objects.first()

    CatalogLockedValidator(catalog)({
        'locked': True
    })


def test_update_unlock(db):
    catalog = Catalog.objects.first()
    catalog.locked = True
    catalog.save()

    CatalogLockedValidator(catalog)({
        'locked': False
    })


def test_serializer_create(db):
    validator = CatalogLockedValidator()
    validator.set_context(CatalogSerializer())

    validator({
        'locked': False
    })


def test_serializer_create_locked(db):
    validator = CatalogLockedValidator()
    validator.set_context(CatalogSerializer())

    validator({
        'locked': True
    })


def test_serializer_update(db):
    catalog = Catalog.objects.first()

    validator = CatalogLockedValidator()
    validator.set_context(CatalogSerializer(instance=catalog))

    validator({})


def test_serializer_update_error(db):
    catalog = Catalog.objects.first()
    catalog.locked = True
    catalog.save()

    validator = CatalogLockedValidator()
    validator.set_context(CatalogSerializer(instance=catalog))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'locked': True
        })


def test_serializer_update_lock(db):
    catalog = Catalog.objects.first()

    validator = CatalogLockedValidator()
    validator.set_context(CatalogSerializer(instance=catalog))

    validator({
        'locked': True
    })


def test_serializer_update_unlock(db):
    catalog = Catalog.objects.first()
    catalog.locked = True
    catalog.save()

    validator = CatalogLockedValidator()
    validator.set_context(CatalogSerializer(instance=catalog))

    validator({
        'locked': False
    })
