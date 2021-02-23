import pytest
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework.exceptions import \
    ValidationError as RestFameworkValidationError

from ..models import Condition
from ..serializers.v1 import ConditionSerializer
from ..validators import ConditionUniqueURIValidator


def test_unique_uri_validator_create(db):
    ConditionUniqueURIValidator()({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'key': 'test'
    })


def test_unique_uri_validator_create_error(db):
    with pytest.raises(ValidationError):
        ConditionUniqueURIValidator()({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'key': Condition.objects.last().key
        })


def test_unique_uri_validator_update(db):
    condition = Condition.objects.first()

    ConditionUniqueURIValidator(condition)({
        'uri_prefix': condition.uri_prefix,
        'key': condition.key
    })


def test_unique_uri_validator_update_error(db):
    condition = Condition.objects.first()

    with pytest.raises(ValidationError):
        ConditionUniqueURIValidator(condition)({
            'uri_prefix': condition.uri_prefix,
            'key': Condition.objects.last().key
        })


def test_unique_uri_validator_serializer_create(db):
    validator = ConditionUniqueURIValidator()
    validator.set_context(ConditionSerializer())

    validator({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'key': 'test'
    })


def test_unique_uri_validator_serializer_create_error(db):
    validator = ConditionUniqueURIValidator()
    validator.set_context(ConditionSerializer())

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'key': Condition.objects.last().key
        })


def test_unique_uri_validator_serializer_update(db):
    condition = Condition.objects.first()

    validator = ConditionUniqueURIValidator()
    validator.set_context(ConditionSerializer(instance=condition))

    validator({
        'uri_prefix': condition.uri_prefix,
        'key': condition.key
    })


def test_unique_uri_validator_serializer_update_error(db):
    condition = Condition.objects.first()

    validator = ConditionUniqueURIValidator()
    validator.set_context(ConditionSerializer(instance=condition))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': condition.uri_prefix,
            'key': Condition.objects.last().key
        })
