import pytest

from django.conf import settings
from django.core.exceptions import ValidationError

from rest_framework.exceptions import ValidationError as RestFameworkValidationError

from ..models import Option, OptionSet
from ..serializers.v1 import OptionSerializer
from ..validators import OptionUniqueURIValidator


def test_unique_uri_validator_create(db):
    OptionUniqueURIValidator()({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'uri_path': 'test'
    })


def test_unique_uri_validator_create_error_option(db):
    with pytest.raises(ValidationError):
        OptionUniqueURIValidator()({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': Option.objects.first().uri_path
        })


def test_unique_uri_validator_create_error_optionset(db):
    with pytest.raises(ValidationError):
        OptionUniqueURIValidator()({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': OptionSet.objects.first().uri_path
        })


def test_unique_uri_validator_update(db):
    instance = Option.objects.first()

    OptionUniqueURIValidator(instance)({
        'uri_prefix': instance.uri_prefix,
        'uri_path': instance.uri_path
    })


def test_unique_uri_validator_update_error_option(db):
    instance = Option.objects.first()

    with pytest.raises(ValidationError):
        OptionUniqueURIValidator(instance)({
            'uri_prefix': instance.uri_prefix,
            'uri_path': Option.objects.exclude(id=instance.id).first().uri_path
        })


def test_unique_uri_validator_update_error_optionset(db):
    instance = Option.objects.first()

    with pytest.raises(ValidationError):
        OptionUniqueURIValidator(instance)({
            'uri_prefix': instance.uri_prefix,
            'uri_path': OptionSet.objects.first().uri_path
        })


def test_unique_uri_validator_serializer_create(db):
    validator = OptionUniqueURIValidator()
    serializer = OptionSerializer()

    validator({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'uri_path': 'test'
    }, serializer)


def test_unique_uri_validator_serializer_create_error(db):
    validator = OptionUniqueURIValidator()
    serializer = OptionSerializer()

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': Option.objects.first().uri_path
        }, serializer)


def test_unique_uri_validator_serializer_update(db):
    instance = Option.objects.first()

    validator = OptionUniqueURIValidator()
    serializer = OptionSerializer(instance=instance)

    validator({
        'uri_prefix': instance.uri_prefix,
        'uri_path': instance.uri_path
    }, serializer)


def test_unique_uri_validator_serializer_update_error(db):
    instance = Option.objects.first()

    validator = OptionUniqueURIValidator()
    serializer = OptionSerializer(instance=instance)

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': instance.uri_prefix,
            'uri_path': Option.objects.exclude(id=instance.id).first().uri_path
        }, serializer)
