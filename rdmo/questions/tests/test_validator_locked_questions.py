import pytest
from django.core.exceptions import ValidationError
from rest_framework.exceptions import \
    ValidationError as RestFameworkValidationError

from ..models import Question, Page
from ..serializers.v1 import QuestionSerializer
from ..validators import QuestionLockedValidator


def test_create(db):
    QuestionLockedValidator()({
        'page': Page.objects.first(),
        'locked': False
    })


def test_create_locked(db):
    QuestionLockedValidator()({
        'page': Page.objects.first(),
        'locked': True
    })


def test_update(db):
    question = Question.objects.exclude(page=None).first()

    QuestionLockedValidator(question)({
        'page': question.page,
        'locked': False
    })


def test_update_error(db):
    question = Question.objects.exclude(page=None).first()
    question.locked = True
    question.save()

    with pytest.raises(ValidationError):
        QuestionLockedValidator(question)({
            'page': question.page,
            'locked': True
        })


def test_update_parent_error(db):
    question = Question.objects.exclude(page=None).first()
    question.page.locked = True
    question.page.save()

    with pytest.raises(ValidationError):
        QuestionLockedValidator(question)({
            'page': question.page,
            'locked': False
        })


def test_update_parent_parent_error(db):
    question = Question.objects.exclude(page=None).first()
    question.page.section.locked = True
    question.page.section.save()

    with pytest.raises(ValidationError):
        QuestionLockedValidator(question)({
            'page': question.page,
            'locked': False
        })


def test_update_parent_parent_parent_error(db):
    question = Question.objects.exclude(page=None).first()
    question.page.section.catalog.locked = True
    question.page.section.catalog.save()

    with pytest.raises(ValidationError):
        QuestionLockedValidator(question)({
            'page': question.page,
            'locked': False
        })


def test_update_lock(db):
    question = Question.objects.exclude(page=None).first()

    QuestionLockedValidator(question)({
        'page': question.page,
        'locked': True
    })


def test_update_unlock(db):
    question = Question.objects.exclude(page=None).first()
    question.locked = True
    question.save()

    QuestionLockedValidator(question)({
        'page': question.page,
        'locked': False
    })


def test_serializer_create(db):
    validator = QuestionLockedValidator()
    validator.set_context(QuestionSerializer())

    validator({
        'page': Page.objects.first(),
        'locked': False
    })


def test_serializer_create_locked(db):
    validator = QuestionLockedValidator()
    validator.set_context(QuestionSerializer())

    validator({
        'page': Page.objects.first(),
        'locked': True
    })


def test_serializer_update(db):
    question = Question.objects.exclude(page=None).first()

    validator = QuestionLockedValidator()
    validator.set_context(QuestionSerializer(instance=question))

    validator({
        'page': question.page,
        'locked': False
    })


def test_serializer_update_error(db):
    question = Question.objects.exclude(page=None).first()
    question.locked = True
    question.save()

    validator = QuestionLockedValidator()
    validator.set_context(QuestionSerializer(instance=question))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'page': question.page,
            'locked': True
        })


def test_serializer_update_parent_error(db):
    question = Question.objects.exclude(page=None).first()
    question.page.locked = True
    question.page.save()

    validator = QuestionLockedValidator()
    validator.set_context(QuestionSerializer(instance=question))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'page': question.page,
            'locked': True
        })


def test_serializer_update_parent_parent_error(db):
    question = Question.objects.exclude(page=None).first()
    question.page.section.locked = True
    question.page.section.save()

    validator = QuestionLockedValidator()
    validator.set_context(QuestionSerializer(instance=question))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'page': question.page,
            'locked': True
        })


def test_serializer_update_parent_parent_parent_error(db):
    question = Question.objects.exclude(page=None).first()
    question.page.section.catalog.locked = True
    question.page.section.catalog.save()

    validator = QuestionLockedValidator()
    validator.set_context(QuestionSerializer(instance=question))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'page': question.page,
            'locked': True
        })


def test_serializer_update_lock(db):
    question = Question.objects.exclude(page=None).first()

    validator = QuestionLockedValidator()
    validator.set_context(QuestionSerializer(instance=question))

    validator({
        'page': question.page,
        'locked': True
    })


def test_serializer_update_unlock(db):
    question = Question.objects.exclude(page=None).first()
    question.locked = True
    question.save()

    validator = QuestionLockedValidator()
    validator.set_context(QuestionSerializer(instance=question))

    validator({
        'page': question.page,
        'locked': False
    })
