import pytest
from django.core.exceptions import ValidationError
from rest_framework.exceptions import \
    ValidationError as RestFameworkValidationError

from ..models import Question, QuestionSet
from ..serializers.v1 import QuestionSerializer
from ..validators import QuestionLockedValidator


def test_create(db):
    QuestionLockedValidator()({
        'questionset': QuestionSet.objects.first(),
        'locked': False
    })


def test_create_locked(db):
    QuestionLockedValidator()({
        'questionset': QuestionSet.objects.first(),
        'locked': True
    })


def test_update(db):
    question = Question.objects.first()

    QuestionLockedValidator(question)({
        'questionset': question.questionset,
        'locked': False
    })


def test_update_error(db):
    question = Question.objects.first()
    question.locked = True
    question.save()

    with pytest.raises(ValidationError):
        QuestionLockedValidator(question)({
            'questionset': question.questionset,
            'locked': True
        })


def test_update_parent_error(db):
    question = Question.objects.first()
    question.questionset.locked = True
    question.questionset.save()

    with pytest.raises(ValidationError):
        QuestionLockedValidator(question)({
            'questionset': question.questionset,
            'locked': False
        })


def test_update_parent_parent_error(db):
    question = Question.objects.first()
    question.questionset.section.locked = True
    question.questionset.section.save()

    with pytest.raises(ValidationError):
        QuestionLockedValidator(question)({
            'questionset': question.questionset,
            'locked': False
        })


def test_update_parent_parent_parent_error(db):
    question = Question.objects.first()
    question.questionset.section.catalog.locked = True
    question.questionset.section.catalog.save()

    with pytest.raises(ValidationError):
        QuestionLockedValidator(question)({
            'questionset': question.questionset,
            'locked': False
        })


def test_update_lock(db):
    question = Question.objects.first()

    QuestionLockedValidator(question)({
        'questionset': question.questionset,
        'locked': True
    })


def test_update_unlock(db):
    question = Question.objects.first()
    question.locked = True
    question.save()

    QuestionLockedValidator(question)({
        'questionset': question.questionset,
        'locked': False
    })


def test_serializer_create(db):
    validator = QuestionLockedValidator()
    validator.set_context(QuestionSerializer())

    validator({
        'questionset': QuestionSet.objects.first(),
        'locked': False
    })


def test_serializer_create_locked(db):
    validator = QuestionLockedValidator()
    validator.set_context(QuestionSerializer())

    validator({
        'questionset': QuestionSet.objects.first(),
        'locked': True
    })


def test_serializer_update(db):
    question = Question.objects.first()

    validator = QuestionLockedValidator()
    validator.set_context(QuestionSerializer(instance=question))

    validator({
        'questionset': question.questionset,
        'locked': False
    })


def test_serializer_update_error(db):
    question = Question.objects.first()
    question.locked = True
    question.save()

    validator = QuestionLockedValidator()
    validator.set_context(QuestionSerializer(instance=question))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'questionset': question.questionset,
            'locked': True
        })


def test_serializer_update_parent_error(db):
    question = Question.objects.first()
    question.questionset.locked = True
    question.questionset.save()

    validator = QuestionLockedValidator()
    validator.set_context(QuestionSerializer(instance=question))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'questionset': question.questionset,
            'locked': True
        })


def test_serializer_update_parent_parent_error(db):
    question = Question.objects.first()
    question.questionset.section.locked = True
    question.questionset.section.save()

    validator = QuestionLockedValidator()
    validator.set_context(QuestionSerializer(instance=question))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'questionset': question.questionset,
            'locked': True
        })


def test_serializer_update_parent_parent_parent_error(db):
    question = Question.objects.first()
    question.questionset.section.catalog.locked = True
    question.questionset.section.catalog.save()

    validator = QuestionLockedValidator()
    validator.set_context(QuestionSerializer(instance=question))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'questionset': question.questionset,
            'locked': True
        })


def test_serializer_update_lock(db):
    question = Question.objects.first()

    validator = QuestionLockedValidator()
    validator.set_context(QuestionSerializer(instance=question))

    validator({
        'questionset': question.questionset,
        'locked': True
    })


def test_serializer_update_unlock(db):
    question = Question.objects.first()
    question.locked = True
    question.save()

    validator = QuestionLockedValidator()
    validator.set_context(QuestionSerializer(instance=question))

    validator({
        'questionset': question.questionset,
        'locked': False
    })
