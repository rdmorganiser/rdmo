import pytest
from django.core.exceptions import ValidationError
from rest_framework.exceptions import \
    ValidationError as RestFameworkValidationError

from ..models import Catalog, Section
from ..serializers.v1 import SectionSerializer
from ..validators import SectionLockedValidator


def test_create(db):
    SectionLockedValidator()({
        'catalog': Catalog.objects.first(),
        'locked': False
    })


def test_create_locked(db):
    SectionLockedValidator()({
        'catalog': Catalog.objects.first(),
        'locked': True
    })


def test_update(db):
    section = Section.objects.first()

    SectionLockedValidator(section)({
        'catalog': section.catalog,
        'locked': False
    })


def test_update_error(db):
    section = Section.objects.first()
    section.locked = True
    section.save()

    with pytest.raises(ValidationError):
        SectionLockedValidator(section)({
            'catalog': section.catalog,
            'locked': True
        })


def test_update_parent_error(db):
    section = Section.objects.first()
    section.catalog.locked = True
    section.catalog.save()

    with pytest.raises(ValidationError):
        SectionLockedValidator(section)({
            'catalog': section.catalog,
            'locked': False
        })


def test_update_lock(db):
    section = Section.objects.first()

    SectionLockedValidator(section)({
        'catalog': section.catalog,
        'locked': True
    })


def test_update_unlock(db):
    section = Section.objects.first()
    section.locked = True
    section.save()

    SectionLockedValidator(section)({
        'catalog': section.catalog,
        'locked': False
    })


def test_serializer_create(db):
    validator = SectionLockedValidator()
    validator.set_context(SectionSerializer())

    validator({
        'catalog': Catalog.objects.first(),
        'locked': False
    })


def test_serializer_create_locked(db):
    validator = SectionLockedValidator()
    validator.set_context(SectionSerializer())

    validator({
        'catalog': Catalog.objects.first(),
        'locked': True
    })


def test_serializer_update(db):
    section = Section.objects.first()

    validator = SectionLockedValidator()
    validator.set_context(SectionSerializer(instance=section))

    validator({
        'catalog': section.catalog,
        'locked': False
    })


def test_serializer_update_error(db):
    section = Section.objects.first()
    section.locked = True
    section.save()

    validator = SectionLockedValidator()
    validator.set_context(SectionSerializer(instance=section))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'catalog': section.catalog,
            'locked': True
        })


def test_serializer_update_parent_error(db):
    section = Section.objects.first()
    section.catalog.locked = True
    section.catalog.save()

    validator = SectionLockedValidator()
    validator.set_context(SectionSerializer(instance=section))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'catalog': section.catalog,
            'locked': True
        })


def test_serializer_update_lock(db):
    section = Section.objects.first()

    validator = SectionLockedValidator()
    validator.set_context(SectionSerializer(instance=section))

    validator({
        'catalog': section.catalog,
        'locked': True
    })


def test_serializer_update_unlock(db):
    section = Section.objects.first()
    section.locked = True
    section.save()

    validator = SectionLockedValidator()
    validator.set_context(SectionSerializer(instance=section))

    validator({
        'catalog': section.catalog,
        'locked': False
    })
