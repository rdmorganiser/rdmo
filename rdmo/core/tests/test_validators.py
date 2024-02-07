import pytest

from django.core.exceptions import ValidationError

from rest_framework import serializers

from ..validators import InstanceValidator


def test_instance_validator():
    validator = InstanceValidator()
    assert validator.instance is None
    assert validator.serializer is None


def test_instance_validator_instance():
    instance = object()
    validator = InstanceValidator(instance)
    assert validator.instance is instance
    assert validator.serializer is None


def test_instance_validator_serializer():
    validator = InstanceValidator()
    serializer = serializers.Serializer()

    validator({}, serializer)

    assert validator.serializer == serializer
    assert validator.serializer.instance is None


def test_instance_validator_serializer_instance():
    validator = InstanceValidator()
    instance = object()
    serializer = serializers.Serializer(instance=instance)

    validator({}, serializer)

    assert validator.serializer == serializer
    assert validator.serializer.instance == serializer.instance


def test_instance_validator_validation_error():
    validator = InstanceValidator()

    with pytest.raises(ValidationError):
        validator.raise_validation_error({
            'foo': 'bar'
        })


def test_instance_validator_validation_serializer_error():
    validator = InstanceValidator()
    serializer = serializers.Serializer()

    validator({}, serializer)

    with pytest.raises(serializers.ValidationError):
        validator.raise_validation_error({
            'foo': 'bar'
        })
