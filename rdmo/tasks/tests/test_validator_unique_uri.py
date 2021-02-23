import pytest
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework.exceptions import \
    ValidationError as RestFameworkValidationError

from ..models import Task
from ..serializers.v1 import TaskSerializer
from ..validators import TaskUniqueURIValidator


def test_unique_uri_validator_create(db):
    TaskUniqueURIValidator()({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'key': 'test'
    })


def test_unique_uri_validator_create_error(db):
    with pytest.raises(ValidationError):
        TaskUniqueURIValidator()({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'key': Task.objects.last().key
        })


def test_unique_uri_validator_update(db):
    task = Task.objects.first()

    TaskUniqueURIValidator(task)({
        'uri_prefix': task.uri_prefix,
        'key': task.key
    })


def test_unique_uri_validator_update_error(db):
    task = Task.objects.first()

    with pytest.raises(ValidationError):
        TaskUniqueURIValidator(task)({
            'uri_prefix': task.uri_prefix,
            'key': Task.objects.last().key
        })


def test_unique_uri_validator_serializer_create(db):
    validator = TaskUniqueURIValidator()
    validator.set_context(TaskSerializer())

    validator({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'key': 'test'
    })


def test_unique_uri_validator_serializer_create_error(db):
    validator = TaskUniqueURIValidator()
    validator.set_context(TaskSerializer())

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'key': Task.objects.last().key
        })


def test_unique_uri_validator_serializer_update(db):
    task = Task.objects.first()

    validator = TaskUniqueURIValidator()
    validator.set_context(TaskSerializer(instance=task))

    validator({
        'uri_prefix': task.uri_prefix,
        'key': task.key
    })


def test_unique_uri_validator_serializer_update_error(db):
    task = Task.objects.first()

    validator = TaskUniqueURIValidator()
    validator.set_context(TaskSerializer(instance=task))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': task.uri_prefix,
            'key': Task.objects.last().key
        })
