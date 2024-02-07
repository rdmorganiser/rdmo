import pytest

from django.conf import settings
from django.core.exceptions import ValidationError

from rest_framework.exceptions import ValidationError as RestFameworkValidationError

from ..models import Option, OptionSet
from ..serializers.v1 import OptionSetSerializer
from ..validators import OptionSetUniqueURIValidator


def test_unique_uri_validator_create(db):
    OptionSetUniqueURIValidator()({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'uri_path': 'test'
    })


def test_unique_uri_validator_create_error_option(db):
    with pytest.raises(ValidationError):
        OptionSetUniqueURIValidator()({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': Option.objects.first().uri_path
        })


def test_unique_uri_validator_create_error_optionset(db):
    with pytest.raises(ValidationError):
        OptionSetUniqueURIValidator()({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': OptionSet.objects.first().uri_path
        })


def test_unique_uri_validator_update(db):
    instance = OptionSet.objects.first()

    OptionSetUniqueURIValidator(instance)({
        'uri_prefix': instance.uri_prefix,
        'uri_path': instance.uri_path
    })


def test_unique_uri_validator_update_error_option(db):
    instance = OptionSet.objects.first()

    with pytest.raises(ValidationError):
        OptionSetUniqueURIValidator(instance)({
            'uri_prefix': instance.uri_prefix,
            'uri_path': Option.objects.first().uri_path
        })


def test_unique_uri_validator_update_error_optionset(db):
    instance = OptionSet.objects.first()

    with pytest.raises(ValidationError):
        OptionSetUniqueURIValidator(instance)({
            'uri_prefix': instance.uri_prefix,
            'uri_path': OptionSet.objects.exclude(id=instance.id).first().uri_path
        })


def test_unique_uri_validator_serializer_create(db):
    validator = OptionSetUniqueURIValidator()
    serializer = OptionSetSerializer()

    validator({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'uri_path': 'test'
    }, serializer)


def test_unique_uri_validator_serializer_create_error(db):
    validator = OptionSetUniqueURIValidator()
    serializer = OptionSetSerializer()

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': OptionSet.objects.first().uri_path
        }, serializer)


def test_unique_uri_validator_serializer_update(db):
    instance = OptionSet.objects.first()

    validator = OptionSetUniqueURIValidator()
    serializer = OptionSetSerializer(instance=instance)

    validator({
        'uri_prefix': instance.uri_prefix,
        'uri_path': instance.uri_path
    }, serializer)


def test_unique_uri_validator_serializer_update_error(db):
    instance = OptionSet.objects.first()

    validator = OptionSetUniqueURIValidator()
    serializer = OptionSetSerializer(instance=instance)

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': instance.uri_prefix,
            'uri_path': OptionSet.objects.exclude(id=instance.id).first().uri_path
        }, serializer)
