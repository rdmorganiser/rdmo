import pytest

from django.conf import settings
from django.core.exceptions import ValidationError

from rest_framework.exceptions import ValidationError as RestFameworkValidationError

from ..models import Task
from ..serializers.v1 import TaskSerializer
from ..validators import TaskUniqueURIValidator


def test_unique_uri_validator_create(db):
    TaskUniqueURIValidator()({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'uri_path': 'test'
    })


def test_unique_uri_validator_create_error(db):
    with pytest.raises(ValidationError):
        TaskUniqueURIValidator()({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': Task.objects.filter(uri_prefix=settings.DEFAULT_URI_PREFIX).last().uri_path
        })


def test_unique_uri_validator_update(db):
    task = Task.objects.first()

    TaskUniqueURIValidator(task)({
        'uri_prefix': task.uri_prefix,
        'uri_path': task.uri_path
    })


def test_unique_uri_validator_update_error(db):
    task = Task.objects.filter(uri_prefix=settings.DEFAULT_URI_PREFIX).first()

    with pytest.raises(ValidationError):
        TaskUniqueURIValidator(task)({
            'uri_prefix': task.uri_prefix,
            'uri_path': Task.objects.filter(uri_prefix=settings.DEFAULT_URI_PREFIX).last().uri_path
        })


def test_unique_uri_validator_serializer_create(db):
    validator = TaskUniqueURIValidator()
    serializer = TaskSerializer()

    validator({
        'uri_prefix': settings.DEFAULT_URI_PREFIX,
        'uri_path': 'test'
    }, serializer)


def test_unique_uri_validator_serializer_create_error(db):
    validator = TaskUniqueURIValidator()
    serializer = TaskSerializer()

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': settings.DEFAULT_URI_PREFIX,
            'uri_path': Task.objects.filter(uri_prefix=settings.DEFAULT_URI_PREFIX).last().uri_path
        }, serializer)


def test_unique_uri_validator_serializer_update(db):
    task = Task.objects.first()

    validator = TaskUniqueURIValidator()
    serializer = TaskSerializer(instance=task)

    validator({
        'uri_prefix': task.uri_prefix,
        'uri_path': task.uri_path
    }, serializer)


def test_unique_uri_validator_serializer_update_error(db):
    task = Task.objects.filter(uri_prefix=settings.DEFAULT_URI_PREFIX).first()

    validator = TaskUniqueURIValidator()
    serializer = TaskSerializer(instance=task)

    with pytest.raises(RestFameworkValidationError):
        validator({
            'uri_prefix': task.uri_prefix,
            'uri_path': Task.objects.filter(uri_prefix=settings.DEFAULT_URI_PREFIX).last().uri_path
        }, serializer)
