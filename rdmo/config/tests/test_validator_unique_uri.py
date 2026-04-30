import pytest

from django.conf import settings
from django.core.exceptions import ValidationError

from rest_framework.exceptions import ValidationError as RestFrameworkValidationError

from ..models import Plugin
from ..serializers.v1 import PluginSerializer
from ..validators import PluginUniqueURIValidator


def test_unique_uri_validator_create(db):
    PluginUniqueURIValidator()({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'uri_path': 'test'
    })


def test_unique_uri_validator_create_error(db):
    with pytest.raises(ValidationError):
        PluginUniqueURIValidator()({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': Plugin.objects.filter(uri_prefix=settings.DEFAULT_URI_PREFIX).last().uri_path
        })


def test_unique_uri_validator_update(db):
    plugin = Plugin.objects.first()

    PluginUniqueURIValidator(plugin)({
        'uri_prefix': plugin.uri_prefix,
        'uri_path': plugin.uri_path
    })


def test_unique_uri_validator_update_error(db):
    plugin = Plugin.objects.filter(uri_prefix=settings.DEFAULT_URI_PREFIX).first()

    with pytest.raises(ValidationError):
        PluginUniqueURIValidator(plugin)({
            'uri_prefix': plugin.uri_prefix,
            'uri_path': Plugin.objects.filter(uri_prefix=settings.DEFAULT_URI_PREFIX).last().uri_path
        })


def test_unique_uri_validator_serializer_create(db):
    validator = PluginUniqueURIValidator()
    serializer = PluginSerializer()

    validator({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'uri_path': 'test'
    }, serializer)


def test_unique_uri_validator_serializer_create_error(db):
    validator = PluginUniqueURIValidator()
    serializer = PluginSerializer()

    with pytest.raises(RestFrameworkValidationError):
        validator({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': Plugin.objects.filter(uri_prefix=settings.DEFAULT_URI_PREFIX).last().uri_path
        }, serializer)


def test_unique_uri_validator_serializer_update(db):
    plugin = Plugin.objects.first()

    validator = PluginUniqueURIValidator()
    serializer = PluginSerializer(instance=plugin)

    validator({
        'uri_prefix': plugin.uri_prefix,
        'uri_path': plugin.uri_path
    }, serializer)


def test_unique_uri_validator_serializer_update_error(db):
    plugin = Plugin.objects.filter(uri_prefix=settings.DEFAULT_URI_PREFIX).first()

    validator = PluginUniqueURIValidator()
    serializer = PluginSerializer(instance=plugin)

    with pytest.raises(RestFrameworkValidationError):
        validator({
            'uri_prefix': plugin.uri_prefix,
            'uri_path': Plugin.objects.filter(uri_prefix=settings.DEFAULT_URI_PREFIX).last().uri_path
        }, serializer)
