import pytest
from django.core.exceptions import ValidationError
from rest_framework.exceptions import \
    ValidationError as RestFameworkValidationError

from ..models import QuestionSet, Page
from ..serializers.v1 import QuestionSetSerializer
from ..validators import QuestionSetLockedValidator


def test_create(db):
    QuestionSetLockedValidator()({
        'page': Page.objects.first(),
        'locked': False
    })


def test_create_locked(db):
    QuestionSetLockedValidator()({
        'page': Page.objects.first(),
        'locked': True
    })


def test_update(db):
    questionset = QuestionSet.objects.exclude(page=None).first()

    QuestionSetLockedValidator(questionset)({
        'page': questionset.page,
        'locked': False
    })


def test_update_error(db):
    questionset = QuestionSet.objects.exclude(page=None).first()
    questionset.locked = True
    questionset.save()

    with pytest.raises(ValidationError):
        QuestionSetLockedValidator(questionset)({
            'page': questionset.page,
            'locked': True
        })


def test_update_parent_error(db):
    questionset = QuestionSet.objects.exclude(page=None).first()
    questionset.page.locked = True
    questionset.page.save()

    with pytest.raises(ValidationError):
        QuestionSetLockedValidator(questionset)({
            'page': questionset.page,
            'locked': False
        })


def test_update_parent_parent_error(db):
    questionset = QuestionSet.objects.exclude(page=None).first()
    questionset.page.section.locked = True
    questionset.page.section.save()

    with pytest.raises(ValidationError):
        QuestionSetLockedValidator(questionset)({
            'page': questionset.page,
            'locked': False
        })


def test_update_lock(db):
    questionset = QuestionSet.objects.exclude(page=None).first()

    QuestionSetLockedValidator(questionset)({
        'page': questionset.page,
        'locked': True
    })


def test_update_unlock(db):
    questionset = QuestionSet.objects.exclude(page=None).first()
    questionset.locked = True
    questionset.save()

    QuestionSetLockedValidator(questionset)({
        'page': questionset.page,
        'locked': False
    })


def test_serializer_create(db):
    validator = QuestionSetLockedValidator()
    validator.set_context(QuestionSetSerializer())

    validator({
        'page': Page.objects.first(),
        'locked': False
    })


def test_serializer_create_locked(db):
    validator = QuestionSetLockedValidator()
    validator.set_context(QuestionSetSerializer())

    validator({
        'page': Page.objects.first(),
        'locked': True
    })


def test_serializer_update(db):
    questionset = QuestionSet.objects.exclude(page=None).first()

    validator = QuestionSetLockedValidator()
    validator.set_context(QuestionSetSerializer(instance=questionset))

    validator({
        'page': questionset.page,
        'locked': False
    })


def test_serializer_update_error(db):
    questionset = QuestionSet.objects.exclude(page=None).first()
    questionset.locked = True
    questionset.save()

    validator = QuestionSetLockedValidator()
    validator.set_context(QuestionSetSerializer(instance=questionset))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'page': questionset.page,
            'locked': True
        })


def test_serializer_update_parent_error(db):
    questionset = QuestionSet.objects.exclude(page=None).first()
    questionset.page.locked = True
    questionset.page.save()

    validator = QuestionSetLockedValidator()
    validator.set_context(QuestionSetSerializer(instance=questionset))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'page': questionset.page,
            'locked': True
        })


def test_serializer_update_parent_parent_error(db):
    questionset = QuestionSet.objects.exclude(page=None).first()
    questionset.page.section.locked = True
    questionset.page.section.save()

    validator = QuestionSetLockedValidator()
    validator.set_context(QuestionSetSerializer(instance=questionset))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'page': questionset.page,
            'locked': True
        })


def test_serializer_update_lock(db):
    questionset = QuestionSet.objects.exclude(page=None).first()

    validator = QuestionSetLockedValidator()
    validator.set_context(QuestionSetSerializer(instance=questionset))

    validator({
        'page': questionset.page,
        'locked': True
    })


def test_serializer_update_unlock(db):
    questionset = QuestionSet.objects.exclude(page=None).first()
    questionset.locked = True
    questionset.save()

    validator = QuestionSetLockedValidator()
    validator.set_context(QuestionSetSerializer(instance=questionset))

    validator({
        'page': questionset.page,
        'locked': False
    })
