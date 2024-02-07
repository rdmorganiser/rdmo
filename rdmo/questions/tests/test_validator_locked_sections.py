import pytest

from django.core.exceptions import ValidationError

from rest_framework.exceptions import ValidationError as RestFameworkValidationError

from ..models import Catalog, Section
from ..serializers.v1 import SectionSerializer
from ..validators import SectionLockedValidator


def test_create(db):
    SectionLockedValidator()({
        'locked': False
    })


def test_create_lock(db):
    SectionLockedValidator()({
        'locked': True
    })


def test_create_catalog(db):
    catalog = Catalog.objects.first()

    SectionLockedValidator()({
        'catalogs': [catalog],
        'locked': False
    })


def test_create_catalog_error(db):
    catalog = Catalog.objects.first()
    catalog.locked = True
    catalog.save()

    with pytest.raises(ValidationError):
        SectionLockedValidator()({
            'catalogs': [catalog],
            'locked': False
        })


def test_update(db):
    section = Section.objects.first()

    SectionLockedValidator(section)({
        'locked': False
    })


def test_update_lock(db):
    section = Section.objects.first()

    SectionLockedValidator(section)({
        'locked': True
    })


def test_update_unlock(db):
    section = Section.objects.first()
    section.locked = True
    section.save()

    SectionLockedValidator(section)({
        'locked': False
    })


def test_update_error(db):
    section = Section.objects.first()
    section.locked = True
    section.save()

    with pytest.raises(ValidationError):
        SectionLockedValidator(section)({
            'locked': True
        })


def test_update_error_catalog(db):
    section = Section.objects.first()
    catalog = section.catalogs.first()
    catalog.locked = True
    catalog.save()

    with pytest.raises(ValidationError):
        SectionLockedValidator(section)({
            'locked': False
        })


def test_update_catalog(db):
    catalog = Catalog.objects.first()

    section = Section.objects.exclude(catalogs=catalog).first()
    SectionLockedValidator(section)({
        'catalogs': [catalog],
        'locked': False
    })


def test_update_catalog_error(db):
    catalog = Catalog.objects.first()
    catalog.locked = True
    catalog.save()

    section = Section.objects.exclude(catalogs=catalog).first()
    with pytest.raises(ValidationError):
        SectionLockedValidator(section)({
            'catalogs': [catalog],
            'locked': False
        })


def test_serializer_create(db):
    validator = SectionLockedValidator()
    serializer = SectionSerializer()

    validator({
        'locked': False
    }, serializer)


def test_serializer_create_locked(db):
    validator = SectionLockedValidator()
    serializer = SectionSerializer()

    validator({
        'locked': True
    }, serializer)


def test_serializer_update(db):
    section = Section.objects.first()

    validator = SectionLockedValidator()
    serializer = SectionSerializer(instance=section)

    validator({
        'locked': False
    }, serializer)


def test_serializer_update_error(db):
    section = Section.objects.first()
    section.locked = True
    section.save()

    validator = SectionLockedValidator()
    serializer = SectionSerializer(instance=section)

    with pytest.raises(RestFameworkValidationError):
        validator({
            'locked': True
        }, serializer)
