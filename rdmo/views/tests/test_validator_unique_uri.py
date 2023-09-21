import pytest

from django.conf import settings
from django.core.exceptions import ValidationError

from rest_framework.exceptions import ValidationError as RestFameworkValidationError

from ..models import View
from ..serializers.v1 import ViewSerializer
from ..validators import ViewUniqueURIValidator


def test_unique_uri_validator_create(db):
    ViewUniqueURIValidator()({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'uri_path': 'test'
    })


def test_unique_uri_validator_create_error(db):
    with pytest.raises(ValidationError):
        ViewUniqueURIValidator()({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': View.objects.filter(uri_prefix=settings.DEFAULT_URI_PREFIX).last().uri_path
        })


def test_unique_uri_validator_update(db):
    view = View.objects.first()

    ViewUniqueURIValidator(view)({
        'uri_prefix': view.uri_prefix,
        'uri_path': view.uri_path
    })


def test_unique_uri_validator_update_error(db):
    view = View.objects.filter(uri_prefix=settings.DEFAULT_URI_PREFIX).first()

    with pytest.raises(ValidationError):
        ViewUniqueURIValidator(view)({
            'uri_prefix': view.uri_prefix,
            'uri_path': View.objects.filter(uri_prefix=settings.DEFAULT_URI_PREFIX).last().uri_path
        })


def test_unique_uri_validator_serializer_create(db):
    validator = ViewUniqueURIValidator()
    serializer = ViewSerializer()

    validator({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'uri_path': 'test'
    }, serializer)


def test_unique_uri_validator_serializer_create_error(db):
    validator = ViewUniqueURIValidator()
    serializer = ViewSerializer()

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': View.objects.filter(uri_prefix=settings.DEFAULT_URI_PREFIX).last().uri_path
        }, serializer)


def test_unique_uri_validator_serializer_update(db):
    view = View.objects.first()

    validator = ViewUniqueURIValidator()
    serializer = ViewSerializer(instance=view)

    validator({
        'uri_prefix': view.uri_prefix,
        'uri_path': view.uri_path
    }, serializer)


def test_unique_uri_validator_serializer_update_error(db):
    view = View.objects.filter(uri_prefix=settings.DEFAULT_URI_PREFIX).first()

    validator = ViewUniqueURIValidator()
    serializer = ViewSerializer(instance=view)

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': view.uri_prefix,
            'uri_path': View.objects.filter(uri_prefix=settings.DEFAULT_URI_PREFIX).last().uri_path
        }, serializer)
