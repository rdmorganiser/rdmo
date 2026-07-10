import pytest

from django.core.exceptions import ValidationError

from rest_framework.exceptions import ValidationError as RestFrameworkValidationError

from ..models import Plugin
from ..serializers.v1 import PluginSerializer
from ..validators import PluginLockedValidator


def test_create(db):
    PluginLockedValidator()({
        'locked': False
    })


def test_create_locked(db):
    PluginLockedValidator()({
        'locked': True
    })


def test_update(db):
    plugin = Plugin.objects.first()

    PluginLockedValidator(plugin)({
        'locked': False
    })


def test_update_error(db):
    plugin = Plugin.objects.first()
    plugin.locked = True
    plugin.save()

    with pytest.raises(ValidationError):
        PluginLockedValidator(plugin)({
            'locked': True
        })


def test_update_lock(db):
    plugin = Plugin.objects.first()

    PluginLockedValidator(plugin)({
        'locked': True
    })


def test_update_unlock(db):
    plugin = Plugin.objects.first()
    plugin.locked = True
    plugin.save()

    PluginLockedValidator(plugin)({
        'locked': False
    })


def test_serializer_create(db):
    validator = PluginLockedValidator()
    serializer = PluginSerializer()

    validator({
        'locked': False
    }, serializer)


def test_serializer_create_locked(db):
    validator = PluginLockedValidator()
    serializer = PluginSerializer()

    validator({
        'locked': True
    }, serializer)


def test_serializer_update(db):
    plugin = Plugin.objects.first()

    validator = PluginLockedValidator()
    serializer = PluginSerializer(instance=plugin)

    validator({}, serializer)


def test_serializer_update_error(db):
    plugin = Plugin.objects.first()
    plugin.locked = True
    plugin.save()

    validator = PluginLockedValidator()
    serializer = PluginSerializer(instance=plugin)

    with pytest.raises(RestFrameworkValidationError):
        validator({
            'locked': True
        }, serializer)


def test_serializer_update_lock(db):
    plugin = Plugin.objects.first()

    validator = PluginLockedValidator()
    serializer = PluginSerializer(instance=plugin)

    validator({
        'locked': True
    }, serializer)


def test_serializer_update_unlock(db):
    plugin = Plugin.objects.first()
    plugin.locked = True
    plugin.save()

    validator = PluginLockedValidator()
    serializer = PluginSerializer(instance=plugin)

    validator({
        'locked': False
    }, serializer)
