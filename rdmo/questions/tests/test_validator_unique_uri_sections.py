import pytest

from django.conf import settings
from django.core.exceptions import ValidationError

from rest_framework.exceptions import ValidationError as RestFameworkValidationError

from ..models import Catalog, Page, Question, QuestionSet, Section
from ..serializers.v1 import SectionSerializer
from ..validators import SectionUniqueURIValidator


def test_unique_uri_validator_create(db):
    SectionUniqueURIValidator()({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'uri_path': 'test'
    })


def test_unique_uri_validator_create_error_question(db):
    with pytest.raises(ValidationError):
        SectionUniqueURIValidator()({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': Question.objects.first().uri_path
        })


def test_unique_uri_validator_create_error_questionset(db):
    with pytest.raises(ValidationError):
        SectionUniqueURIValidator()({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': QuestionSet.objects.first().uri_path
        })


def test_unique_uri_validator_create_error_page(db):
    with pytest.raises(ValidationError):
        SectionUniqueURIValidator()({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': Page.objects.first().uri_path
        })


def test_unique_uri_validator_create_error_section(db):
    with pytest.raises(ValidationError):
        SectionUniqueURIValidator()({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': Section.objects.first().uri_path
        })


def test_unique_uri_validator_create_error_catalog(db):
    with pytest.raises(ValidationError):
        SectionUniqueURIValidator()({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': Catalog.objects.first().uri_path
        })


def test_unique_uri_validator_update(db):
    instance = Section.objects.first()

    SectionUniqueURIValidator(instance)({
        'uri_prefix': instance.uri_prefix,
        'uri_path': instance.uri_path
    })


def test_unique_uri_validator_update_error_question(db):
    instance = Section.objects.first()

    with pytest.raises(ValidationError):
        SectionUniqueURIValidator(instance)({
            'uri_prefix': instance.uri_prefix,
            'uri_path': Question.objects.exclude(id=instance.id).first().uri_path
        })


def test_unique_uri_validator_update_error_questionset(db):
    instance = Section.objects.first()

    with pytest.raises(ValidationError):
        SectionUniqueURIValidator(instance)({
            'uri_prefix': instance.uri_prefix,
            'uri_path': QuestionSet.objects.first().uri_path
        })


def test_unique_uri_validator_update_error_page(db):
    instance = Section.objects.first()

    with pytest.raises(ValidationError):
        SectionUniqueURIValidator(instance)({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': Page.objects.first().uri_path
        })


def test_unique_uri_validator_update_error_section(db):
    instance = Section.objects.first()

    with pytest.raises(ValidationError):
        SectionUniqueURIValidator(instance)({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': Section.objects.exclude(id=instance.id).first().uri_path
        })


def test_unique_uri_validator_update_error_catalog(db):
    instance = Section.objects.first()

    with pytest.raises(ValidationError):
        SectionUniqueURIValidator(instance)({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': Catalog.objects.first().uri_path
        })


def test_unique_uri_validator_serializer_create(db):
    validator = SectionUniqueURIValidator()
    serializer = SectionSerializer()

    validator({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'uri_path': 'test'
    }, serializer)


def test_unique_uri_validator_serializer_create_error(db):
    validator = SectionUniqueURIValidator()
    serializer = SectionSerializer()

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': Section.objects.first().uri_path
        }, serializer)


def test_unique_uri_validator_serializer_update(db):
    instance = Section.objects.first()

    validator = SectionUniqueURIValidator()
    serializer = SectionSerializer(instance=instance)

    validator({
        'uri_prefix': instance.uri_prefix,
        'uri_path': instance.uri_path
    }, serializer)


def test_unique_uri_validator_serializer_update_error(db):
    instance = Section.objects.first()

    validator = SectionUniqueURIValidator()
    serializer = SectionSerializer(instance=instance)

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': instance.uri_prefix,
            'uri_path': Section.objects.exclude(id=instance.id).first().uri_path
        }, serializer)
