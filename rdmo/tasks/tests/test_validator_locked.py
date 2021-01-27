import pytest
from django.core.exceptions import ValidationError
from rest_framework.exceptions import \
    ValidationError as RestFameworkValidationError

from ..models import Task
from ..serializers.v1 import TaskSerializer
from ..validators import TaskLockedValidator


def test_create(db):
    TaskLockedValidator()({
        'locked': False
    })


def test_create_locked(db):
    TaskLockedValidator()({
        'locked': True
    })


def test_update(db):
    task = Task.objects.first()

    TaskLockedValidator(task)({
        'locked': False
    })


def test_update_error(db):
    task = Task.objects.first()
    task.locked = True
    task.save()

    with pytest.raises(ValidationError):
        TaskLockedValidator(task)({
            'locked': True
        })


def test_update_lock(db):
    task = Task.objects.first()

    TaskLockedValidator(task)({
        'locked': True
    })


def test_update_unlock(db):
    task = Task.objects.first()
    task.locked = True
    task.save()

    TaskLockedValidator(task)({
        'locked': False
    })


def test_serializer_create(db):
    validator = TaskLockedValidator()
    validator.set_context(TaskSerializer())

    validator({
        'locked': False
    })


def test_serializer_create_locked(db):
    validator = TaskLockedValidator()
    validator.set_context(TaskSerializer())

    validator({
        'locked': True
    })


def test_serializer_update(db):
    task = Task.objects.first()

    validator = TaskLockedValidator()
    validator.set_context(TaskSerializer(instance=task))

    validator({})


def test_serializer_update_error(db):
    task = Task.objects.first()
    task.locked = True
    task.save()

    validator = TaskLockedValidator()
    validator.set_context(TaskSerializer(instance=task))

    with pytest.raises(RestFameworkValidationError):
        validator({
            'locked': True
        })


def test_serializer_update_lock(db):
    task = Task.objects.first()

    validator = TaskLockedValidator()
    validator.set_context(TaskSerializer(instance=task))

    validator({
        'locked': True
    })


def test_serializer_update_unlock(db):
    task = Task.objects.first()
    task.locked = True
    task.save()

    validator = TaskLockedValidator()
    validator.set_context(TaskSerializer(instance=task))

    validator({
        'locked': False
    })
