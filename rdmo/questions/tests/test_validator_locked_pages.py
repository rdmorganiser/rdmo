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
    questionset = Page.objects.first()

    PageLockedValidator(questionset)({
        'section': questionset.section,
        'locked': False
    })


def test_update_error(db):
    questionset = Page.objects.first()
    questionset.locked = True
    questionset.save()

    with pytest.raises(ValidationError):
        PageLockedValidator(questionset)({
            'section': questionset.section,
            'locked': True
        })


def test_update_parent_error(db):
    questionset = Page.objects.first()
    questionset.section.locked = True
    questionset.section.save()

    with pytest.raises(ValidationError):
        PageLockedValidator(questionset)({
            'section': questionset.section,
            'locked': False
        })


def test_update_parent_parent_error(db):
    questionset = Page.objects.first()
    questionset.section.catalog.locked = True
    questionset.section.catalog.save()

    with pytest.raises(ValidationError):
        PageLockedValidator(questionset)({
            'section': questionset.section,
            'locked': False
        })


def test_update_lock(db):
    questionset = Page.objects.first()

    PageLockedValidator(questionset)({
        'section': questionset.section,
        'locked': True
    })


def test_update_unlock(db):
    questionset = Page.objects.first()
    questionset.locked = True
    questionset.save()

    PageLockedValidator(questionset)({
        'section': questionset.section,
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
    questionset = Page.objects.first()

    validator = PageLockedValidator()
    validator.set_context(PageSerializer(instance=questionset))

    validator({
        'section': questionset.section,
        'locked': False
    })


def test_serializer_update_error(db):
    questionset = Page.objects.first()
    questionset.locked = True
    questionset.save()

    validator = PageLockedValidator()
    validator.set_context(PageSerializer(instance=questionset))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'section': questionset.section,
            'locked': True
        })


def test_serializer_update_parent_error(db):
    questionset = Page.objects.first()
    questionset.section.locked = True
    questionset.section.save()

    validator = PageLockedValidator()
    validator.set_context(PageSerializer(instance=questionset))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'section': questionset.section,
            'locked': True
        })


def test_serializer_update_parent_parent_error(db):
    questionset = Page.objects.first()
    questionset.section.catalog.locked = True
    questionset.section.catalog.save()

    validator = PageLockedValidator()
    validator.set_context(PageSerializer(instance=questionset))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'section': questionset.section,
            'locked': True
        })


def test_serializer_update_lock(db):
    questionset = Page.objects.first()

    validator = PageLockedValidator()
    validator.set_context(PageSerializer(instance=questionset))

    validator({
        'section': questionset.section,
        'locked': True
    })


def test_serializer_update_unlock(db):
    questionset = Page.objects.first()
    questionset.locked = True
    questionset.save()

    validator = PageLockedValidator()
    validator.set_context(PageSerializer(instance=questionset))

    validator({
        'section': questionset.section,
        'locked': False
    })
