import pytest

from django.core.exceptions import ValidationError

from rest_framework.exceptions import ValidationError as RestFameworkValidationError

from ..models import Page, QuestionSet
from ..serializers.v1 import QuestionSetSerializer
from ..validators import QuestionSetLockedValidator


def test_create(db):
    QuestionSetLockedValidator()({
        'locked': False
    })


def test_create_locked(db):
    QuestionSetLockedValidator()({
        'locked': True
    })


def test_create_page(db):
    page = Page.objects.first()

    QuestionSetLockedValidator()({
        'pages': [page],
        'locked': False
    })


def test_create_page_error(db):
    page = Page.objects.first()
    page.locked = True
    page.save()

    with pytest.raises(ValidationError):
        QuestionSetLockedValidator()({
            'pages': [page],
            'locked': False
        })


def test_create_page_error_section(db):
    page = Page.objects.first()
    section = page.sections.first()
    section.locked = True
    section.save()

    with pytest.raises(ValidationError):
        QuestionSetLockedValidator()({
            'pages': [page],
            'locked': False
        })


def test_create_page_error_catalog(db):
    page = Page.objects.first()
    section = page.sections.first()
    catalog = section.catalogs.first()
    catalog.locked = True
    catalog.save()

    with pytest.raises(ValidationError):
        QuestionSetLockedValidator()({
            'pages': [page],
            'locked': False
        })


def test_create_questionset(db):
    questionset = QuestionSet.objects.first()

    QuestionSetLockedValidator()({
        'parents': [questionset],
        'locked': False
    })


def test_create_questionset_error(db):
    questionset = QuestionSet.objects.exclude(pages=None).first()
    questionset.locked = True
    questionset.save()

    with pytest.raises(ValidationError):
        QuestionSetLockedValidator()({
            'parents': [questionset],
            'locked': False
        })


def test_create_questionset_page(db):
    questionset = QuestionSet.objects.exclude(pages=None).first()
    page = questionset.pages.first()
    page.locked = True
    page.save()

    with pytest.raises(ValidationError):
        QuestionSetLockedValidator()({
            'parents': [questionset],
            'locked': False
        })


def test_create_questionset_error_section(db):
    questionset = QuestionSet.objects.exclude(pages=None).first()
    page = questionset.pages.first()
    section = page.sections.first()
    section.locked = True
    section.save()

    with pytest.raises(ValidationError):
        QuestionSetLockedValidator()({
            'parents': [questionset],
            'locked': False
        })


def test_create_questionset_error_catalog(db):
    questionset = QuestionSet.objects.exclude(pages=None).first()
    page = questionset.pages.first()
    section = page.sections.first()
    catalog = section.catalogs.first()
    catalog.locked = True
    catalog.save()

    with pytest.raises(ValidationError):
        QuestionSetLockedValidator()({
            'parents': [questionset],
            'locked': False
        })


def test_update(db):
    instance = QuestionSet.objects.first()

    QuestionSetLockedValidator(instance)({
        'locked': False
    })


def test_update_error(db):
    instance = QuestionSet.objects.first()
    instance.locked = True
    instance.save()

    with pytest.raises(ValidationError):
        QuestionSetLockedValidator(instance)({
            'locked': True
        })


def test_update_lock(db):
    instance = QuestionSet.objects.first()

    QuestionSetLockedValidator(instance)({
        'locked': True
    })


def test_update_unlock(db):
    instance = QuestionSet.objects.first()
    instance.locked = True
    instance.save()

    QuestionSetLockedValidator(instance)({
        'locked': False
    })


def test_update_error_page(db):
    instance = QuestionSet.objects.exclude(pages=None).first()
    page = instance.pages.first()
    page.locked = True
    page.save()

    with pytest.raises(ValidationError):
        QuestionSetLockedValidator(instance)({
            'locked': False
        })


def test_update_error_page_section(db):
    instance = QuestionSet.objects.exclude(pages=None).first()
    page = instance.pages.first()
    section = page.sections.first()
    section.locked = True
    section.save()

    with pytest.raises(ValidationError):
        QuestionSetLockedValidator(instance)({
            'locked': False
        })


def test_update_error_page_catalog(db):
    instance = QuestionSet.objects.exclude(pages=None).first()
    page = instance.pages.first()
    section = page.sections.first()
    catalog = section.catalogs.first()
    catalog.locked = True
    catalog.save()

    with pytest.raises(ValidationError):
        QuestionSetLockedValidator(instance)({
            'locked': False
        })


def test_update_error_questionset(db):
    instance = QuestionSet.objects.exclude(parents=None).first()
    questionset = instance.parents.first()
    questionset.locked = True
    questionset.save()

    with pytest.raises(ValidationError):
        QuestionSetLockedValidator(instance)({
            'locked': False
        })


def test_update_page(db):
    page = Page.objects.first()

    instance = QuestionSet.objects.exclude(pages=page).first()
    QuestionSetLockedValidator(instance)({
        'pages': [page],
        'locked': False
    })


def test_update_page_error(db):
    page = Page.objects.first()
    page.locked = True
    page.save()

    instance = QuestionSet.objects.exclude(pages=page).first()
    with pytest.raises(ValidationError):
        QuestionSetLockedValidator(instance)({
            'pages': [page],
            'locked': False
        })


def test_update_page_error_section(db):
    page = Page.objects.first()
    section = page.sections.first()
    section.locked = True
    section.save()

    instance = QuestionSet.objects.exclude(pages=page).first()
    with pytest.raises(ValidationError):
        QuestionSetLockedValidator(instance)({
            'pages': [page],
            'locked': False
        })


def test_update_page_error_catalog(db):
    page = Page.objects.first()
    section = page.sections.first()
    catalog = section.catalogs.first()
    catalog.locked = True
    catalog.save()

    instance = QuestionSet.objects.exclude(pages=page).first()
    with pytest.raises(ValidationError):
        QuestionSetLockedValidator(instance)({
            'pages': [page],
            'locked': False
        })


def test_update_questionset(db):
    questionset = QuestionSet.objects.first()

    instance = QuestionSet.objects.exclude(questionsets=questionset).first()
    QuestionSetLockedValidator(instance)({
        'parents': [questionset],
        'locked': False
    })


def test_update_questionset_error(db):
    questionset = QuestionSet.objects.first()
    questionset.locked = True
    questionset.save()

    instance = QuestionSet.objects.exclude(questionsets=questionset).first()
    with pytest.raises(ValidationError):
        QuestionSetLockedValidator(instance)({
            'parents': [questionset],
            'locked': False
        })


def test_update_questionset_error_questionset(db):
    questionset = QuestionSet.objects.exclude(questionsets=None).first()
    questionset_questionset = questionset.questionsets.first()
    questionset_questionset.locked = True
    questionset_questionset.save()

    instance = QuestionSet.objects.exclude(questionsets=questionset).first()
    with pytest.raises(ValidationError):
        QuestionSetLockedValidator(instance)({
            'parents': [questionset],
            'locked': False
        })


def test_update_questionset_error_page(db):
    questionset = QuestionSet.objects.exclude(pages=None).first()
    page = questionset.pages.first()
    page.locked = True
    page.save()

    instance = QuestionSet.objects.exclude(questionsets=questionset).first()
    with pytest.raises(ValidationError):
        QuestionSetLockedValidator(instance)({
            'parents': [questionset],
            'locked': False
        })


def test_update_questionset_error_section(db):
    questionset = QuestionSet.objects.exclude(pages=None).first()
    page = questionset.pages.first()
    section = page.sections.first()
    section.locked = True
    section.save()

    instance = QuestionSet.objects.exclude(questionsets=questionset).first()
    with pytest.raises(ValidationError):
        QuestionSetLockedValidator(instance)({
            'parents': [questionset],
            'locked': False
        })


def test_update_questionset_error_catalog(db):
    questionset = QuestionSet.objects.exclude(pages=None).first()
    page = questionset.pages.first()
    section = page.sections.first()
    catalog = section.catalogs.first()
    catalog.locked = True
    catalog.save()

    instance = QuestionSet.objects.exclude(questionsets=questionset).first()
    with pytest.raises(ValidationError):
        QuestionSetLockedValidator(instance)({
            'parents': [questionset],
            'locked': False
        })


def test_serializer_create(db):
    validator = QuestionSetLockedValidator()
    serializer = QuestionSetSerializer()

    validator({
        'locked': False
    }, serializer)


def test_serializer_create_locked(db):
    validator = QuestionSetLockedValidator()
    serializer = QuestionSetSerializer()

    validator({
        'locked': True
    }, serializer)


def test_serializer_update(db):
    instance = QuestionSet.objects.first()

    validator = QuestionSetLockedValidator()
    serializer = QuestionSetSerializer(instance=instance)

    validator({
        'locked': False
    }, serializer)


def test_serializer_update_error(db):
    instance = QuestionSet.objects.first()
    instance.locked = True
    instance.save()

    validator = QuestionSetLockedValidator()
    serializer = QuestionSetSerializer(instance=instance)

    with pytest.raises(RestFameworkValidationError):
        validator({
            'locked': True
        }, serializer)
