import pytest

from django.conf import settings
from django.core.exceptions import ValidationError

from rest_framework.exceptions import ValidationError as RestFameworkValidationError

from ..models import Catalog, Page, Question, QuestionSet, Section
from ..serializers.v1 import PageSerializer
from ..validators import PageUniqueURIValidator


def test_unique_uri_validator_create(db):
    PageUniqueURIValidator()({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'uri_path': 'test'
    })


def test_unique_uri_validator_create_error_question(db):
    with pytest.raises(ValidationError):
        PageUniqueURIValidator()({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': Question.objects.first().uri_path
        })


def test_unique_uri_validator_create_error_questionset(db):
    with pytest.raises(ValidationError):
        PageUniqueURIValidator()({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': QuestionSet.objects.first().uri_path
        })


def test_unique_uri_validator_create_error_page(db):
    with pytest.raises(ValidationError):
        PageUniqueURIValidator()({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': Page.objects.first().uri_path
        })


def test_unique_uri_validator_create_error_section(db):
    with pytest.raises(ValidationError):
        PageUniqueURIValidator()({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': Section.objects.first().uri_path
        })


def test_unique_uri_validator_create_error_catalog(db):
    with pytest.raises(ValidationError):
        PageUniqueURIValidator()({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': Catalog.objects.first().uri_path
        })


def test_unique_uri_validator_update(db):
    instance = Page.objects.first()

    PageUniqueURIValidator(instance)({
        'uri_prefix': instance.uri_prefix,
        'uri_path': instance.uri_path
    })


def test_unique_uri_validator_update_error_question(db):
    instance = Catalog.objects.first()

    with pytest.raises(ValidationError):
        PageUniqueURIValidator(instance)({
            'uri_prefix': instance.uri_prefix,
            'uri_path': Question.objects.first().uri_path
        })


def test_unique_uri_validator_update_error_questionset(db):
    instance = Catalog.objects.first()

    with pytest.raises(ValidationError):
        PageUniqueURIValidator(instance)({
            'uri_prefix': instance.uri_prefix,
            'uri_path': QuestionSet.objects.first().uri_path
        })


def test_unique_uri_validator_update_error_page(db):
    instance = Page.objects.first()

    with pytest.raises(ValidationError):
        PageUniqueURIValidator(instance)({
            'uri_prefix': instance.uri_prefix,
            'uri_path': Page.objects.exclude(id=instance.id).first().uri_path
        })


def test_unique_uri_validator_update_error_section(db):
    instance = Page.objects.first()

    with pytest.raises(ValidationError):
        PageUniqueURIValidator(instance)({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': Section.objects.first().uri_path
        })


def test_unique_uri_validator_update_error_catalog(db):
    instance = Page.objects.first()

    with pytest.raises(ValidationError):
        PageUniqueURIValidator(instance)({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': Catalog.objects.first().uri_path
        })


def test_unique_uri_validator_serializer_create(db):
    validator = PageUniqueURIValidator()
    serializer = PageSerializer()

    validator({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'uri_path': 'test'
    }, serializer)


def test_unique_uri_validator_serializer_create_error(db):
    validator = PageUniqueURIValidator()
    serializer = PageSerializer()

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': Page.objects.first().uri_path
        }, serializer)


def test_unique_uri_validator_serializer_update(db):
    instance = Page.objects.first()

    validator = PageUniqueURIValidator()
    serializer = PageSerializer(instance=instance)

    validator({
        'uri_prefix': instance.uri_prefix,
        'uri_path': instance.uri_path
    }, serializer)


def test_unique_uri_validator_serializer_update_error(db):
    instance = Page.objects.first()

    validator = PageUniqueURIValidator()
    serializer = PageSerializer(instance=instance)

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': instance.uri_prefix,
            'uri_path': Page.objects.exclude(id=instance.id).first().uri_path
        }, serializer)
