import pytest
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework.exceptions import \
    ValidationError as RestFameworkValidationError

from ..models import QuestionSet, Section
from ..serializers.v1 import QuestionSetSerializer
from ..validators import QuestionSetUniqueURIValidator


def test_unique_uri_validator_create(db):
    QuestionSetUniqueURIValidator()({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'key': 'test',
        'section': Section.objects.first()
    })


def test_unique_uri_validator_create_error(db):
    section = Section.objects.first()

    with pytest.raises(ValidationError):
        QuestionSetUniqueURIValidator()({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'key': section.questionsets.first().key,
            'section': section
        })


def test_unique_uri_validator_update(db):
    questionset = QuestionSet.objects.first()

    QuestionSetUniqueURIValidator(questionset)({
        'uri_prefix': questionset.uri_prefix,
        'key': questionset.key,
        'section': questionset.section
    })


def test_unique_uri_validator_update_error(db):
    questionset = QuestionSet.objects.first()

    with pytest.raises(ValidationError):
        QuestionSetUniqueURIValidator(questionset)({
            'uri_prefix': questionset.uri_prefix,
            'key': questionset.section.questionsets.last().key,
            'section': questionset.section
        })


def test_unique_uri_validator_serializer_create(db):
    validator = QuestionSetUniqueURIValidator()
    validator.set_context(QuestionSetSerializer())

    validator({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'key': 'test',
        'section': Section.objects.first()
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


def test_unique_uri_validator_serializer_update(db):
    questionset = QuestionSet.objects.first()

    validator = QuestionSetUniqueURIValidator()
    validator.set_context(QuestionSetSerializer(instance=questionset))

    validator({
        'uri_prefix': questionset.uri_prefix,
        'key': questionset.key,
        'section': questionset.section
    })


def test_unique_uri_validator_serializer_update_error(db):
    questionset = QuestionSet.objects.first()

    validator = QuestionSetUniqueURIValidator()
    validator.set_context(QuestionSetSerializer(instance=questionset))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': questionset.uri_prefix,
            'key': questionset.section.questionsets.last().key,
            'section': questionset.section
        })
