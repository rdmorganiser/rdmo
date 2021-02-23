import pytest
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework.exceptions import \
    ValidationError as RestFameworkValidationError

from ..models import Catalog
from ..serializers.v1 import CatalogSerializer
from ..validators import CatalogUniqueURIValidator


def test_unique_uri_validator_create(db):
    CatalogUniqueURIValidator()({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'key': 'test'
    })


def test_unique_uri_validator_create_error(db):
    with pytest.raises(ValidationError):
        CatalogUniqueURIValidator()({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'key': Catalog.objects.get(pk=2).key
        })


def test_unique_uri_validator_update(db):
    catalog = Catalog.objects.get(pk=1)

    CatalogUniqueURIValidator(catalog)({
        'uri_prefix': catalog.uri_prefix,
        'key': catalog.key
    })


def test_unique_uri_validator_update_error(db):
    catalog = Catalog.objects.get(pk=1)

    with pytest.raises(ValidationError):
        CatalogUniqueURIValidator(catalog)({
            'uri_prefix': catalog.uri_prefix,
            'key': Catalog.objects.get(pk=2).key
        })


def test_unique_uri_validator_serializer_create(db):
    validator = CatalogUniqueURIValidator()
    validator.set_context(CatalogSerializer())

    validator({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'key': 'test'
    })


def test_unique_uri_validator_serializer_create_error(db):
    validator = CatalogUniqueURIValidator()
    validator.set_context(CatalogSerializer())

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'key': Catalog.objects.get(pk=2).key
        })


def test_unique_uri_validator_serializer_update(db):
    catalog = Catalog.objects.get(pk=1)

    validator = CatalogUniqueURIValidator()
    validator.set_context(CatalogSerializer(instance=catalog))

    validator({
        'uri_prefix': catalog.uri_prefix,
        'key': catalog.key
    })


def test_unique_uri_validator_serializer_update_error(db):
    catalog = Catalog.objects.get(pk=1)

    validator = CatalogUniqueURIValidator()
    validator.set_context(CatalogSerializer(instance=catalog))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': catalog.uri_prefix,
            'key': Catalog.objects.get(pk=2).key
        })
