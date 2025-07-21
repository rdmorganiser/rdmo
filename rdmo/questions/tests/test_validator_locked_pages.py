import pytest

from django.core.exceptions import ValidationError

from rest_framework.exceptions import ValidationError as RestFrameworkValidationError

from ..models import Page, Section
from ..serializers.v1 import PageSerializer
from ..validators import PageLockedValidator


def test_create(db):
    PageLockedValidator()({
        'locked': False
    })


def test_create_lock(db):
    PageLockedValidator()({
        'locked': True
    })


def test_create_section(db):
    section = Section.objects.first()

    PageLockedValidator()({
        'sections': [section],
        'locked': False
    })


def test_create_section_error(db):
    section = Section.objects.first()
    section.locked = True
    section.save()

    with pytest.raises(ValidationError):
        PageLockedValidator()({
            'sections': [section],
            'locked': False
        })


def test_create_section_error_catalog(db):
    section = Section.objects.first()
    catalog = section.catalogs.first()
    catalog.locked = True
    catalog.save()

    with pytest.raises(ValidationError):
        PageLockedValidator()({
            'sections': [section],
            'locked': False
        })


def test_update(db):
    page = Page.objects.first()

    PageLockedValidator(page)({
        'locked': False
    })


def test_update_lock(db):
    page = Page.objects.first()

    PageLockedValidator(page)({
        'locked': True
    })


def test_update_unlock(db):
    page = Page.objects.first()
    page.locked = True
    page.save()

    PageLockedValidator(page)({
        'locked': False
    })


def test_update_error(db):
    page = Page.objects.first()
    page.locked = True
    page.save()

    with pytest.raises(ValidationError):
        PageLockedValidator(page)({
            'locked': True
        })


def test_update_error_section(db):
    page = Page.objects.first()
    section = page.sections.first()
    section.locked = True
    section.save()

    with pytest.raises(ValidationError):
        PageLockedValidator(page)({
            'locked': False
        })


def test_update_error_catalog(db):
    page = Page.objects.first()
    section = page.sections.first()
    catalog = section.catalogs.first()
    catalog.locked = True
    catalog.save()

    with pytest.raises(ValidationError):
        PageLockedValidator(page)({
            'locked': False
        })


def test_update_section(db):
    page = Page.objects.first()
    section = Section.objects.first()

    PageLockedValidator(page)({
        'sections': [section],
        'locked': False
    })


def test_update_section_error(db):
    section = Section.objects.first()
    section.locked = True
    section.save()

    page = Page.objects.exclude(sections=section).first()
    with pytest.raises(ValidationError):
        PageLockedValidator(page)({
            'sections': [section],
            'locked': False
        })


def test_update_section_error_catalog(db):
    section = Section.objects.first()
    catalog = section.catalogs.first()
    catalog.locked = True
    catalog.save()

    page = Page.objects.exclude(sections=section).first()
    with pytest.raises(ValidationError):
        PageLockedValidator(page)({
            'sections': [section],
            'locked': False
        })


def test_serializer_create(db):
    validator = PageLockedValidator()
    serializer = PageSerializer()

    validator({
        'locked': False
    }, serializer)


def test_serializer_create_locked(db):
    validator = PageLockedValidator()
    serializer = PageSerializer()

    validator({
        'locked': True
    }, serializer)


def test_serializer_update(db):
    page = Page.objects.first()

    validator = PageLockedValidator()
    serializer = PageSerializer(instance=page)

    validator({
        'locked': False
    }, serializer)


def test_serializer_update_error(db):
    page = Page.objects.first()
    page.locked = True
    page.save()

    validator = PageLockedValidator()
    serializer = PageSerializer(instance=page)

    with pytest.raises(RestFrameworkValidationError):
        validator({
            'locked': True
        }, serializer)
