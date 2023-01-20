import pytest
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework.exceptions import \
    ValidationError as RestFameworkValidationError

from ..models import Question, QuestionSet, Page, Catalog, Section
from ..serializers.v1 import QuestionSetSerializer
from ..validators import QuestionSetUniqueURIValidator


def test_unique_uri_validator_create(db):
    QuestionSetUniqueURIValidator()({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'key': 'test',
        'section': Section.objects.first()
    })


def test_unique_uri_validator_create2(db):
    section = Section.objects.first()
    questionset = section.questionsets.first()

def test_unique_uri_validator_create_error_questionset(db):
    with pytest.raises(ValidationError):
        QuestionSetUniqueURIValidator()({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': QuestionSet.objects.first().uri_path
        })


def test_unique_uri_validator_create_error(db):
    section = Section.objects.first()

def test_unique_uri_validator_create_error_page(db):
    with pytest.raises(ValidationError):
        QuestionSetUniqueURIValidator()({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': Page.objects.first().uri_path
        })


def test_unique_uri_validator_create_error2(db):
    section = Section.objects.first()
    questionset = section.questionsets.first()

    with pytest.raises(ValidationError):
        QuestionSetUniqueURIValidator()({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': Section.objects.first().uri_path
        })


def test_unique_uri_validator_create_error_catalog(db):
    with pytest.raises(ValidationError):
        QuestionSetUniqueURIValidator()({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': Catalog.objects.first().uri_path
        })


def test_unique_uri_validator_update(db):
    instance = QuestionSet.objects.filter(uri_prefix=settings.DEFAULT_URI_PREFIX).first()

    QuestionSetUniqueURIValidator(instance)({
        'uri_prefix': instance.uri_prefix,
        'uri_path': instance.uri_path
    })


def test_unique_uri_validator_update_error_question(db):
    instance = QuestionSet.objects.first()

    with pytest.raises(ValidationError):
        QuestionSetUniqueURIValidator(instance)({
            'uri_prefix': instance.uri_prefix,
            'uri_path': Question.objects.first().uri_path
        })


def test_unique_uri_validator_update_error_questionset(db):
    instance = QuestionSet.objects.first()

    with pytest.raises(ValidationError):
        QuestionSetUniqueURIValidator(instance)({
            'uri_prefix': instance.uri_prefix,
            'uri_path': QuestionSet.objects.exclude(id=instance.id).first().uri_path
        })


def test_unique_uri_validator_update_error_page(db):
    instance = QuestionSet.objects.first()

    with pytest.raises(ValidationError):
        QuestionSetUniqueURIValidator(instance)({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': Page.objects.first().uri_path
        })


def test_unique_uri_validator_update_error_section(db):
    instance = QuestionSet.objects.first()

    with pytest.raises(ValidationError):
        QuestionSetUniqueURIValidator(instance)({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': Section.objects.first().uri_path
        })


def test_unique_uri_validator_update_error_catalog(db):
    instance = QuestionSet.objects.filter(uri_prefix=settings.DEFAULT_URI_PREFIX).first()

    with pytest.raises(ValidationError):
        QuestionSetUniqueURIValidator(instance)({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': Catalog.objects.first().uri_path
        })


def test_unique_uri_validator_serializer_create(db):
    validator = QuestionSetUniqueURIValidator()
    validator.set_context(QuestionSetSerializer())

    validator({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'key': 'test',
        'section': Section.objects.first()
    })


def test_unique_uri_validator_serializer_create2(db):
    section = Section.objects.first()
    questionset = section.questionsets.first()

    validator = QuestionSetUniqueURIValidator()
    validator.set_context(QuestionSetSerializer())

    validator({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'key': 'test',
        'section': section,
        'questionset': questionset
    })


def test_unique_uri_validator_serializer_create_error(db):
    section = Section.objects.first()

    validator = QuestionSetUniqueURIValidator()
    validator.set_context(QuestionSetSerializer())

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'key': section.questionsets.last().key,
            'section': section
        })


def test_unique_uri_validator_serializer_create_error2(db):
    section = Section.objects.first()
    questionset = section.questionsets.first()

    validator = QuestionSetUniqueURIValidator()
    validator.set_context(QuestionSetSerializer())

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'key': questionset.questions.first().key,
            'section': section,
            'questionset': questionset,
        })


def test_unique_uri_validator_serializer_create_error3(db):
    # get a questionset which contains a questionset
    questionset = QuestionSet.objects.exclude(questionset=None).first().questionset

    validator = QuestionSetUniqueURIValidator()
    validator.set_context(QuestionSetSerializer())

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'key': questionset.questions.first().key,
            'section': questionset.section,
            'questionset': questionset,
        })


def test_unique_uri_validator_serializer_update(db):
    questionset = QuestionSet.objects.first()

    validator = QuestionSetUniqueURIValidator()
    validator.set_context(QuestionSetSerializer(instance=instance))

    validator({
        'uri_prefix': instance.uri_prefix,
        'uri_path': instance.uri_path
    })


def test_unique_uri_validator_serializer_update_error(db):
    questionset = QuestionSet.objects.first()

    validator = QuestionSetUniqueURIValidator()
    validator.set_context(QuestionSetSerializer(instance=instance))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': instance.uri_prefix,
            'uri_path': QuestionSet.objects.exclude(id=instance.id).first().uri_path
        })
