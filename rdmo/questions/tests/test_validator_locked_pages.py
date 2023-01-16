import pytest
from django.core.exceptions import ValidationError
from rest_framework.exceptions import \
    ValidationError as RestFameworkValidationError

from ..models import Page, Section
from ..serializers.v1 import PageSerializer
from ..validators import PageLockedValidator


def test_create(db):
    PageLockedValidator()({
        'section': Section.objects.first(),
        'locked': False
    })


def test_create_locked(db):
    PageLockedValidator()({
        'section': Section.objects.first(),
        'locked': True
    })


def test_update(db):
    page = Page.objects.first()

    PageLockedValidator(page)({
        'section': page.section,
        'locked': False
    })


def test_update_error(db):
    page = Page.objects.first()
    page.locked = True
    page.save()

    with pytest.raises(ValidationError):
        PageLockedValidator(page)({
            'section': page.section,
            'locked': True
        })


def test_update_parent_error(db):
    page = Page.objects.first()
    page.section.locked = True
    page.section.save()

    with pytest.raises(ValidationError):
        PageLockedValidator(page)({
            'section': page.section,
            'locked': False
        })


def test_update_parent_parent_error(db):
    page = Page.objects.first()
    page.section.catalog.locked = True
    page.section.catalog.save()

    with pytest.raises(ValidationError):
        PageLockedValidator(page)({
            'section': page.section,
            'locked': False
        })


def test_update_lock(db):
    page = Page.objects.first()

    PageLockedValidator(page)({
        'section': page.section,
        'locked': True
    })


def test_update_unlock(db):
    page = Page.objects.first()
    page.locked = True
    page.save()

    PageLockedValidator(page)({
        'section': page.section,
        'locked': False
    })


def test_serializer_create(db):
    validator = PageLockedValidator()
    validator.set_context(PageSerializer())

    validator({
        'section': Section.objects.first(),
        'locked': False
    })


def test_serializer_create_locked(db):
    validator = PageLockedValidator()
    validator.set_context(PageSerializer())

    validator({
        'section': Section.objects.first(),
        'locked': True
    })


def test_serializer_update(db):
    page = Page.objects.first()

    validator = PageLockedValidator()
    validator.set_context(PageSerializer(instance=page))

    validator({
        'section': page.section,
        'locked': False
    })


def test_serializer_update_error(db):
    page = Page.objects.first()
    page.locked = True
    page.save()

    validator = PageLockedValidator()
    validator.set_context(PageSerializer(instance=page))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'section': page.section,
            'locked': True
        })


def test_serializer_update_parent_error(db):
    page = Page.objects.first()
    page.section.locked = True
    page.section.save()

    validator = PageLockedValidator()
    validator.set_context(PageSerializer(instance=page))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'section': page.section,
            'locked': True
        })


def test_serializer_update_parent_parent_error(db):
    page = Page.objects.first()
    page.section.catalog.locked = True
    page.section.catalog.save()

    validator = PageLockedValidator()
    validator.set_context(PageSerializer(instance=page))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'section': page.section,
            'locked': True
        })


def test_serializer_update_lock(db):
    page = Page.objects.first()

    validator = PageLockedValidator()
    validator.set_context(PageSerializer(instance=page))

    validator({
        'section': page.section,
        'locked': True
    })


def test_serializer_update_unlock(db):
    page = Page.objects.first()
    page.locked = True
    page.save()

    validator = PageLockedValidator()
    validator.set_context(PageSerializer(instance=page))

    validator({
        'section': page.section,
        'locked': False
    })
