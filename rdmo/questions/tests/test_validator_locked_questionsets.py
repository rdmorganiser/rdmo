import pytest
from django.core.exceptions import ValidationError
from rest_framework.exceptions import \
    ValidationError as RestFameworkValidationError

from ..models import QuestionSet, Section
from ..serializers.v1 import QuestionSetSerializer
from ..validators import QuestionSetLockedValidator


def test_create(db):
    QuestionSetLockedValidator()({
        'section': Section.objects.first(),
        'locked': False
    })


def test_create_locked(db):
    QuestionSetLockedValidator()({
        'section': Section.objects.first(),
        'locked': True
    })


def test_update(db):
    questionset = QuestionSet.objects.first()

    QuestionSetLockedValidator(questionset)({
        'section': questionset.section,
        'locked': False
    })


def test_update_error(db):
    questionset = QuestionSet.objects.first()
    questionset.locked = True
    questionset.save()

    with pytest.raises(ValidationError):
        QuestionSetLockedValidator(questionset)({
            'section': questionset.section,
            'locked': True
        })


def test_update_parent_error(db):
    questionset = QuestionSet.objects.first()
    questionset.section.locked = True
    questionset.section.save()

    with pytest.raises(ValidationError):
        QuestionSetLockedValidator(questionset)({
            'section': questionset.section,
            'locked': False
        })


def test_update_parent_parent_error(db):
    questionset = QuestionSet.objects.first()
    questionset.section.catalog.locked = True
    questionset.section.catalog.save()

    with pytest.raises(ValidationError):
        QuestionSetLockedValidator(questionset)({
            'section': questionset.section,
            'locked': False
        })


def test_update_lock(db):
    questionset = QuestionSet.objects.first()

    QuestionSetLockedValidator(questionset)({
        'section': questionset.section,
        'locked': True
    })


def test_update_unlock(db):
    questionset = QuestionSet.objects.first()
    questionset.locked = True
    questionset.save()

    QuestionSetLockedValidator(questionset)({
        'section': questionset.section,
        'locked': False
    })


def test_serializer_create(db):
    validator = QuestionSetLockedValidator()
    validator.set_context(QuestionSetSerializer())

    validator({
        'section': Section.objects.first(),
        'locked': False
    })


def test_serializer_create_locked(db):
    validator = QuestionSetLockedValidator()
    validator.set_context(QuestionSetSerializer())

    validator({
        'section': Section.objects.first(),
        'locked': True
    })


def test_serializer_update(db):
    questionset = QuestionSet.objects.first()

    validator = QuestionSetLockedValidator()
    validator.set_context(QuestionSetSerializer(instance=questionset))

    validator({
        'section': questionset.section,
        'locked': False
    })


def test_serializer_update_error(db):
    questionset = QuestionSet.objects.first()
    questionset.locked = True
    questionset.save()

    validator = QuestionSetLockedValidator()
    validator.set_context(QuestionSetSerializer(instance=questionset))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'section': questionset.section,
            'locked': True
        })


def test_serializer_update_parent_error(db):
    questionset = QuestionSet.objects.first()
    questionset.section.locked = True
    questionset.section.save()

    validator = QuestionSetLockedValidator()
    validator.set_context(QuestionSetSerializer(instance=questionset))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'section': questionset.section,
            'locked': True
        })


def test_serializer_update_parent_parent_error(db):
    questionset = QuestionSet.objects.first()
    questionset.section.catalog.locked = True
    questionset.section.catalog.save()

    validator = QuestionSetLockedValidator()
    validator.set_context(QuestionSetSerializer(instance=questionset))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'section': questionset.section,
            'locked': True
        })


def test_serializer_update_lock(db):
    questionset = QuestionSet.objects.first()

    validator = QuestionSetLockedValidator()
    validator.set_context(QuestionSetSerializer(instance=questionset))

    validator({
        'section': questionset.section,
        'locked': True
    })


def test_serializer_update_unlock(db):
    questionset = QuestionSet.objects.first()
    questionset.locked = True
    questionset.save()

    validator = QuestionSetLockedValidator()
    validator.set_context(QuestionSetSerializer(instance=questionset))

    validator({
        'section': questionset.section,
        'locked': False
    })
