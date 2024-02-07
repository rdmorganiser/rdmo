from datetime import timedelta

import pytest

from rest_framework.exceptions import ValidationError as RestFameworkValidationError

from ..models import Project, Value
from ..serializers.v1 import ValueSerializer
from ..validators import ValueConflictValidator

project_id = 1
attribute_path = attribute__path='individual/single/text'


def test_serializer_create(db):
    class MockedView:
        project = Project.objects.get(id=project_id)

    value = Value.objects.get(project_id=project_id, snapshot=None, attribute__path=attribute_path)

    validator = ValueConflictValidator()
    serializer = ValueSerializer()
    serializer.context['view'] = MockedView()

    validator({
        'attribute': value.attribute,
        'set_prefix': value.set_prefix,
        'set_index': value.set_index,
        'collection_index': value.collection_index + 1,
    }, serializer)


def test_serializer_create_error(db):
    class MockedView:
        project = Project.objects.get(id=project_id)

    value = Value.objects.get(project_id=project_id, snapshot=None, attribute__path=attribute_path)

    validator = ValueConflictValidator()
    serializer = ValueSerializer()
    serializer.context['view'] = MockedView()

    with pytest.raises(RestFameworkValidationError):
        validator({
            'attribute': value.attribute,
            'set_prefix': value.set_prefix,
            'set_index': value.set_index,
            'collection_index': value.collection_index,
        }, serializer)


def test_serializer_update(db):
    value = Value.objects.get(project_id=project_id, snapshot=None, attribute__path=attribute_path)

    class MockedRequest:
        data = {
            'updated': value.updated .isoformat()
        }

    class MockedView:
        request = MockedRequest()
        project = Project.objects.get(id=project_id)

    validator = ValueConflictValidator()
    serializer = ValueSerializer()
    serializer.instance = value
    serializer.context['view'] = MockedView()

    validator({
        'attribute': value.attribute,
        'set_prefix': value.set_prefix,
        'set_index': value.set_index,
        'collection_index': value.collection_index,
    }, serializer)


def test_serializer_update_error(db):
    value = Value.objects.get(project_id=project_id, snapshot=None, attribute__path=attribute_path)

    class MockedRequest:
        data = {
            'updated': (value.updated - timedelta(seconds=1)).isoformat()
        }

    class MockedView:
        request = MockedRequest()
        project = Project.objects.get(id=project_id)

    validator = ValueConflictValidator()
    serializer = ValueSerializer()
    serializer.instance = value
    serializer.context['view'] = MockedView()

    with pytest.raises(RestFameworkValidationError):
        validator({
            'attribute': value.attribute,
            'set_prefix': value.set_prefix,
            'set_index': value.set_index,
            'collection_index': value.collection_index,
        }, serializer)


def test_serializer_update_missing_updated(db):
    value = Value.objects.get(project_id=project_id, snapshot=None, attribute__path=attribute_path)

    class MockedRequest:
        data = {}

    class MockedView:
        request = MockedRequest()
        project = Project.objects.get(id=project_id)

    validator = ValueConflictValidator()
    serializer = ValueSerializer()
    serializer.instance = value
    serializer.context['view'] = MockedView()

    validator({
        'attribute': value.attribute,
        'set_prefix': value.set_prefix,
        'set_index': value.set_index,
        'collection_index': value.collection_index,
    }, serializer)
