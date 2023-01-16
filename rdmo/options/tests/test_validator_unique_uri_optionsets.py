import pytest
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework.exceptions import \
    ValidationError as RestFameworkValidationError

from ..models import OptionSet, Option
from ..serializers.v1 import OptionSetSerializer
from ..validators import OptionSetUniqueURIValidator


def test_unique_uri_validator_create(db):
    OptionSetUniqueURIValidator()({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'uri_path': 'test'
    })


def test_unique_uri_validator_create_error(db):
    with pytest.raises(ValidationError):
        OptionSetUniqueURIValidator()({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': OptionSet.objects.first().uri_path
        })


def test_unique_uri_validator_create_option_error(db):
    with pytest.raises(ValidationError):
        OptionSetUniqueURIValidator()({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': Option.objects.first().uri_path
        })


def test_unique_uri_validator_update(db):
    optionset = OptionSet.objects.first()

    OptionSetUniqueURIValidator(optionset)({
        'uri_prefix': optionset.uri_prefix,
        'uri_path': optionset.uri_path
    })


def test_unique_uri_validator_update_error(db):
    optionset = OptionSet.objects.first()

    with pytest.raises(ValidationError):
        OptionSetUniqueURIValidator(optionset)({
            'uri_prefix': optionset.uri_prefix,
            'uri_path': OptionSet.objects.exclude(id=optionset.id).first().uri_path
        })


def test_unique_uri_validator_update_option_error(db):
    optionset = OptionSet.objects.first()

    with pytest.raises(ValidationError):
        OptionSetUniqueURIValidator(optionset)({
            'uri_prefix': optionset.uri_prefix,
            'uri_path': Option.objects.first().uri_path
        })


def test_unique_uri_validator_serializer_create(db):
    validator = OptionSetUniqueURIValidator()
    validator.set_context(OptionSetSerializer())

    validator({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'uri_path': 'test'
    })


def test_unique_uri_validator_serializer_create_error(db):
    validator = OptionSetUniqueURIValidator()
    validator.set_context(OptionSetSerializer())

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': OptionSet.objects.first().uri_path
        })


def test_unique_uri_validator_serializer_create_option_error(db):
    validator = OptionSetUniqueURIValidator()
    validator.set_context(OptionSetSerializer())

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': Option.objects.first().uri_path
        })


def test_unique_uri_validator_serializer_update(db):
    optionset = OptionSet.objects.first()

    validator = OptionSetUniqueURIValidator()
    validator.set_context(OptionSetSerializer(instance=optionset))

    validator({
        'uri_prefix': optionset.uri_prefix,
        'uri_path': optionset.uri_path
    })


def test_unique_uri_validator_serializer_update_error(db):
    optionset = OptionSet.objects.first()

    validator = OptionSetUniqueURIValidator()
    validator.set_context(OptionSetSerializer(instance=optionset))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': optionset.uri_prefix,
            'uri_path': OptionSet.objects.exclude(id=optionset.id).first().uri_path
        })


def test_unique_uri_validator_serializer_update_option_error(db):
    optionset = OptionSet.objects.first()

    validator = OptionSetUniqueURIValidator()
    validator.set_context(OptionSetSerializer(instance=optionset))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': optionset.uri_prefix,
            'uri_path': Option.objects.first().uri_path
        })
