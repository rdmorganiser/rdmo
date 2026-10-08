from unittest.mock import Mock

import pytest

from django.core.exceptions import ValidationError

from rest_framework import serializers

from ..validators import InstanceValidator


def test_empty():
    validator = InstanceValidator()
    assert validator.instance is None


def test_not_implemented():
    validator = InstanceValidator()
    serializer = serializers.Serializer()

    with pytest.raises(NotImplementedError):
        validator({}, serializer)


def test_get_instance():
    instance = Mock()
    validator = InstanceValidator(instance)
    assert validator.instance is instance
    assert validator.get_instance(None) is instance


def test_get_instance_serializer():
    validator = InstanceValidator()
    instance = Mock()
    serializer = serializers.Serializer(instance=instance)
    assert validator.instance is None
    assert validator.get_instance(serializer) is instance


def test_get_instance_none():
    validator = InstanceValidator()
    assert validator.instance is None
    assert validator.get_instance(None) is None


def test_get_value_data():
    validator = InstanceValidator()
    data = {
        'foo': 'bar'
    }
    assert validator.get_value(data, None, 'foo') == 'bar'


def test_get_value_instance():
    validator = InstanceValidator()
    data = {}
    instance = Mock()
    instance.foo = 'baz'
    assert validator.get_value(data, instance, 'foo') == 'baz'


def test_get_value_data_instance():
    validator = InstanceValidator()
    data = {
        'foo': 'bar'
    }
    instance = Mock()
    instance.foo = 'baz'
    assert validator.get_value(data, instance, 'foo') == 'bar'


def test_raise_validation_error():
    validator = InstanceValidator()

    with pytest.raises(ValidationError):
        validator.raise_validation_error({
            'foo': 'bar'
        })
