import pytest
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework.exceptions import \
    ValidationError as RestFameworkValidationError

from ..models import Catalog, Section
from ..serializers.v1 import SectionSerializer
from ..validators import SectionUniqueURIValidator


def test_unique_uri_validator_create(db):
    SectionUniqueURIValidator()({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'key': 'test',
        'catalog': Catalog.objects.first()
    })


def test_unique_uri_validator_create_error(db):
    catalog = Catalog.objects.first()

    with pytest.raises(ValidationError):
        SectionUniqueURIValidator()({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'key': catalog.sections.first().key,
            'catalog': catalog
        })


def test_unique_uri_validator_update(db):
    section = Section.objects.first()

    SectionUniqueURIValidator(section)({
        'uri_prefix': section.uri_prefix,
        'key': section.key,
        'catalog': section.catalog
    })


def test_unique_uri_validator_update_error(db):
    section = Section.objects.first()

    with pytest.raises(ValidationError):
        SectionUniqueURIValidator(section)({
            'uri_prefix': section.uri_prefix,
            'key': section.catalog.sections.last().key,
            'catalog': section.catalog
        })


def test_unique_uri_validator_serializer_create(db):
    validator = SectionUniqueURIValidator()
    validator.set_context(SectionSerializer())

    validator({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'key': 'test',
        'catalog': Catalog.objects.first()
    })


def test_unique_uri_validator_serializer_create_error(db):
    catalog = Catalog.objects.first()

    validator = SectionUniqueURIValidator()
    validator.set_context(SectionSerializer())

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'key': catalog.sections.last().key,
            'catalog': catalog
        })


def test_unique_uri_validator_serializer_update(db):
    section = Section.objects.first()

    validator = SectionUniqueURIValidator()
    validator.set_context(SectionSerializer(instance=section))

    validator({
        'uri_prefix': section.uri_prefix,
        'key': section.key,
        'catalog': section.catalog
    })


def test_unique_uri_validator_serializer_update_error(db):
    section = Section.objects.first()

    validator = SectionUniqueURIValidator()
    validator.set_context(SectionSerializer(instance=section))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': section.uri_prefix,
            'key': section.catalog.sections.last().key,
            'catalog': section.catalog
        })
