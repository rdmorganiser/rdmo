import pytest
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework.exceptions import \
    ValidationError as RestFameworkValidationError

from ..models import Option, OptionSet
from ..serializers.v1 import OptionSerializer
from ..validators import OptionUniqueURIValidator


def test_unique_uri_validator_create(db):
    OptionUniqueURIValidator()({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'uri_path': 'test'
    })


def test_unique_uri_validator_create_error(db):
    with pytest.raises(ValidationError):
        OptionUniqueURIValidator()({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': Option.objects.first().uri_path
        })


def test_unique_uri_validator_create_optioset_error(db):
    with pytest.raises(ValidationError):
        OptionUniqueURIValidator()({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': OptionSet.objects.first().uri_path
        })


def test_unique_uri_validator_update(db):
    option = Option.objects.first()

    OptionUniqueURIValidator(option)({
        'uri_prefix': option.uri_prefix,
        'uri_path': option.uri_path
    })


def test_unique_uri_validator_update_error(db):
    option = Option.objects.first()

    with pytest.raises(ValidationError):
        OptionUniqueURIValidator(option)({
            'uri_prefix': option.uri_prefix,
            'uri_path': Option.objects.exclude(id=option.id).first().uri_path
        })


def test_unique_uri_validator_update_optionset_error(db):
    option = Option.objects.first()

    with pytest.raises(ValidationError):
        OptionUniqueURIValidator(option)({
            'uri_prefix': option.uri_prefix,
            'uri_path': OptionSet.objects.first().uri_path
        })


def test_unique_uri_validator_serializer_create(db):
    validator = OptionUniqueURIValidator()
    validator.set_context(OptionSerializer())

    validator({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'uri_path': 'test'
    })


def test_unique_uri_validator_serializer_create_error(db):
    validator = OptionUniqueURIValidator()
    validator.set_context(OptionSerializer())

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': OptionSet.objects.first().uri_path
        })


def test_unique_uri_validator_serializer_create_option_error(db):
    validator = OptionUniqueURIValidator()
    validator.set_context(OptionSerializer())

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': Option.objects.first().uri_path
        })


def test_unique_uri_validator_serializer_update(db):
    option = Option.objects.first()

    validator = OptionUniqueURIValidator()
    validator.set_context(OptionSerializer(instance=option))

    validator({
        'uri_prefix': option.uri_prefix,
        'uri_path': option.uri_path
    })


def test_unique_uri_validator_serializer_update_error(db):
    option = Option.objects.first()

    validator = OptionUniqueURIValidator()
    validator.set_context(OptionSerializer(instance=option))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': option.uri_prefix,
            'uri_path': Option.objects.exclude(id=option.id).first().uri_path
        })


def test_unique_uri_validator_serializer_update_optionset_error(db):
    option = Option.objects.first()

    validator = OptionUniqueURIValidator()
    validator.set_context(OptionSerializer(instance=option))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': option.uri_prefix,
            'uri_path': OptionSet.objects.first().uri_path
        })
