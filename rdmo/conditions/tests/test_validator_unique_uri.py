import pytest

from django.conf import settings
from django.core.exceptions import ValidationError

from rest_framework.exceptions import ValidationError as RestFameworkValidationError

from ..models import Condition
from ..serializers.v1 import ConditionSerializer
from ..validators import ConditionUniqueURIValidator


def test_unique_uri_validator_create(db):
    ConditionUniqueURIValidator()({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'uri_path': 'test'
    })


def test_unique_uri_validator_create_error(db):
    with pytest.raises(ValidationError):
        ConditionUniqueURIValidator()({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': Condition.objects.filter(uri_prefix=settings.DEFAULT_URI_PREFIX).last().uri_path
        })


def test_unique_uri_validator_update(db):
    condition = Condition.objects.first()

    ConditionUniqueURIValidator(condition)({
        'uri_prefix': condition.uri_prefix,
        'uri_path': condition.uri_path
    })


def test_unique_uri_validator_update_error(db):
    condition = Condition.objects.filter(uri_prefix=settings.DEFAULT_URI_PREFIX).first()

    with pytest.raises(ValidationError):
        ConditionUniqueURIValidator(condition)({
            'uri_prefix': condition.uri_prefix,
            'uri_path': Condition.objects.filter(uri_prefix=settings.DEFAULT_URI_PREFIX).last().uri_path
        })


def test_unique_uri_validator_serializer_create(db):
    validator = ConditionUniqueURIValidator()
    serializer = ConditionSerializer()

    validator({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'uri_path': 'test'
    }, serializer)


def test_unique_uri_validator_serializer_create_error(db):
    validator = ConditionUniqueURIValidator()
    serializer = ConditionSerializer()

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': Condition.objects.filter(uri_prefix=settings.DEFAULT_URI_PREFIX).last().uri_path
        }, serializer)


def test_unique_uri_validator_serializer_update(db):
    condition = Condition.objects.first()

    validator = ConditionUniqueURIValidator()
    serializer = ConditionSerializer(instance=condition)

    validator({
        'uri_prefix': condition.uri_prefix,
        'uri_path': condition.uri_path
    }, serializer)


def test_unique_uri_validator_serializer_update_error(db):
    condition = Condition.objects.filter(uri_prefix=settings.DEFAULT_URI_PREFIX).first()

    validator = ConditionUniqueURIValidator()
    serializer = ConditionSerializer(instance=condition)

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': condition.uri_prefix,
            'uri_path': Condition.objects.filter(uri_prefix=settings.DEFAULT_URI_PREFIX).last().uri_path
        }, serializer)
