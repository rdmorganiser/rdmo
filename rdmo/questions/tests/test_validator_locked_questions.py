import pytest

from django.core.exceptions import ValidationError

from rest_framework.exceptions import ValidationError as RestFameworkValidationError

from ..models import Page, Question, QuestionSet
from ..serializers.v1 import QuestionSerializer
from ..validators import QuestionLockedValidator


def test_create(db):
    QuestionLockedValidator()({
        'locked': False
    })


def test_create_locked(db):
    QuestionLockedValidator()({
        'locked': True
    })


def test_create_page(db):
    page = Page.objects.first()

    QuestionLockedValidator()({
        'pages': [page],
        'locked': False
    })


def test_create_page_error(db):
    page = Page.objects.first()
    page.locked = True
    page.save()

    with pytest.raises(ValidationError):
        QuestionLockedValidator()({
            'pages': [page],
            'locked': False
        })


def test_create_page_error_section(db):
    page = Page.objects.first()
    section = page.sections.first()
    section.locked = True
    section.save()

    with pytest.raises(ValidationError):
        QuestionLockedValidator()({
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
        QuestionLockedValidator()({
            'pages': [page],
            'locked': False
        })


def test_create_questionset(db):
    questionset = QuestionSet.objects.first()

    QuestionLockedValidator()({
        'questionsets': [questionset],
        'locked': False
    })


def test_create_questionset_error(db):
    questionset = QuestionSet.objects.exclude(pages=None).first()
    questionset.locked = True
    questionset.save()

    with pytest.raises(ValidationError):
        QuestionLockedValidator()({
            'questionsets': [questionset],
            'locked': False
        })


def test_create_questionset_page(db):
    questionset = QuestionSet.objects.exclude(pages=None).first()
    page = questionset.pages.first()
    page.locked = True
    page.save()

    with pytest.raises(ValidationError):
        QuestionLockedValidator()({
            'questionsets': [questionset],
            'locked': False
        })


def test_create_questionset_error_section(db):
    questionset = QuestionSet.objects.exclude(pages=None).first()
    page = questionset.pages.first()
    section = page.sections.first()
    section.locked = True
    section.save()

    with pytest.raises(ValidationError):
        QuestionLockedValidator()({
            'questionsets': [questionset],
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
        QuestionLockedValidator()({
            'questionsets': [questionset],
            'locked': False
        })


def test_update(db):
    question = Question.objects.first()

    QuestionLockedValidator(question)({
        'locked': False
    })


def test_update_lock(db):
    question = Question.objects.first()

    QuestionLockedValidator(question)({
        'locked': True
    })


def test_update_unlock(db):
    question = Question.objects.first()
    question.locked = True
    question.save()

    QuestionLockedValidator(question)({
        'locked': False
    })


def test_update_error(db):
    question = Question.objects.first()
    question.locked = True
    question.save()

    with pytest.raises(ValidationError):
        QuestionLockedValidator(question)({
            'locked': True
        })


def test_update_error_page(db):
    question = Question.objects.exclude(pages=None).first()
    page = question.pages.first()
    page.locked = True
    page.save()

    with pytest.raises(ValidationError):
        QuestionLockedValidator(question)({
            'locked': False
        })


def test_update_error_page_section(db):
    question = Question.objects.exclude(pages=None).first()
    page = question.pages.first()
    section = page.sections.first()
    section.locked = True
    section.save()

    with pytest.raises(ValidationError):
        QuestionLockedValidator(question)({
            'locked': False
        })


def test_update_error_page_catalog(db):
    question = Question.objects.exclude(pages=None).first()
    page = question.pages.first()
    section = page.sections.first()
    catalog = section.catalogs.first()
    catalog.locked = True
    catalog.save()

    with pytest.raises(ValidationError):
        QuestionLockedValidator(question)({
            'locked': False
        })


def test_update_error_questionset(db):
    question = Question.objects.exclude(questionsets=None).first()
    questionset = question.questionsets.first()
    questionset.locked = True
    questionset.save()

    with pytest.raises(ValidationError):
        QuestionLockedValidator(question)({
            'locked': False
        })


def test_update_error_questionset_page(db):
    question = Question.objects.exclude(questionsets=None).first()
    questionset = question.questionsets.first()
    page = questionset.pages.first()
    page.locked = True
    page.save()

    with pytest.raises(ValidationError):
        QuestionLockedValidator(question)({
            'locked': False
        })


def test_update_error_questionset_section(db):
    question = Question.objects.exclude(questionsets=None).first()
    questionset = question.questionsets.first()
    page = questionset.pages.first()
    section = page.sections.first()
    section.locked = True
    section.save()

    with pytest.raises(ValidationError):
        QuestionLockedValidator(question)({
            'locked': False
        })


def test_update_error_questionset_catalog(db):
    question = Question.objects.exclude(questionsets=None).first()
    questionset = question.questionsets.first()
    page = questionset.pages.first()
    section = page.sections.first()
    catalog = section.catalogs.first()
    catalog.locked = True
    catalog.save()

    with pytest.raises(ValidationError):
        QuestionLockedValidator(question)({
            'locked': False
        })


def test_update_page(db):
    page = Page.objects.first()

    question = Question.objects.exclude(pages=page).first()
    QuestionLockedValidator(question)({
        'pages': [page],
        'locked': False
    })


def test_update_page_error(db):
    page = Page.objects.first()
    page.locked = True
    page.save()

    question = Question.objects.exclude(pages=page).first()
    with pytest.raises(ValidationError):
        QuestionLockedValidator(question)({
            'pages': [page],
            'locked': False
        })


def test_update_page_error_section(db):
    page = Page.objects.first()
    section = page.sections.first()
    section.locked = True
    section.save()

    question = Question.objects.exclude(pages=page).first()
    with pytest.raises(ValidationError):
        QuestionLockedValidator(question)({
            'pages': [page],
            'locked': False
        })


def test_update_page_error_catalog(db):
    page = Page.objects.first()
    section = page.sections.first()
    catalog = section.catalogs.first()
    catalog.locked = True
    catalog.save()

    question = Question.objects.exclude(pages=page).first()
    with pytest.raises(ValidationError):
        QuestionLockedValidator(question)({
            'pages': [page],
            'locked': False
        })


def test_update_questionset(db):
    questionset = QuestionSet.objects.first()

    question = Question.objects.exclude(questionsets=questionset).first()
    QuestionLockedValidator(question)({
        'questionsets': [questionset],
        'locked': False
    })


def test_update_questionset_error(db):
    questionset = QuestionSet.objects.first()
    questionset.locked = True
    questionset.save()

    question = Question.objects.exclude(questionsets=questionset).first()
    with pytest.raises(ValidationError):
        QuestionLockedValidator(question)({
            'questionsets': [questionset],
            'locked': False
        })


def test_update_questionset_error_questionset(db):
    questionset = QuestionSet.objects.exclude(questionsets=None).first()
    questionset_questionset = questionset.questionsets.first()
    questionset_questionset.locked = True
    questionset_questionset.save()

    question = Question.objects.exclude(questionsets=questionset).first()
    with pytest.raises(ValidationError):
        QuestionLockedValidator(question)({
            'questionsets': [questionset],
            'locked': False
        })


def test_update_questionset_error_page(db):
    questionset = QuestionSet.objects.exclude(pages=None).first()
    page = questionset.pages.first()
    page.locked = True
    page.save()

    question = Question.objects.exclude(questionsets=questionset).first()
    with pytest.raises(ValidationError):
        QuestionLockedValidator(question)({
            'questionsets': [questionset],
            'locked': False
        })


def test_update_questionset_error_section(db):
    questionset = QuestionSet.objects.exclude(pages=None).first()
    page = questionset.pages.first()
    section = page.sections.first()
    section.locked = True
    section.save()

    question = Question.objects.exclude(questionsets=questionset).first()
    with pytest.raises(ValidationError):
        QuestionLockedValidator(question)({
            'questionsets': [questionset],
            'locked': False
        })


def test_update_questionset_error_catalog(db):
    questionset = QuestionSet.objects.exclude(pages=None).first()
    page = questionset.pages.first()
    section = page.sections.first()
    catalog = section.catalogs.first()
    catalog.locked = True
    catalog.save()

    question = Question.objects.exclude(questionsets=questionset).first()
    with pytest.raises(ValidationError):
        QuestionLockedValidator(question)({
            'questionsets': [questionset],
            'locked': False
        })


def test_serializer_create(db):
    validator = QuestionLockedValidator()
    serializer = QuestionSerializer()

    validator({
        'locked': False
    }, serializer)


def test_serializer_create_locked(db):
    validator = QuestionLockedValidator()
    serializer = QuestionSerializer()

    validator({
        'locked': True
    }, serializer)


def test_serializer_update(db):
    question = Question.objects.first()

    validator = QuestionLockedValidator()
    serializer = QuestionSerializer(instance=question)

    validator({
        'locked': False
    }, serializer)


def test_serializer_update_error(db):
    question = Question.objects.first()
    question.locked = True
    question.save()

    validator = QuestionLockedValidator()
    serializer = QuestionSerializer(instance=question)

    with pytest.raises(RestFameworkValidationError):
        validator({
            'locked': True
        }, serializer)
