from datetime import timedelta

import pytest

from rest_framework.exceptions import ValidationError as RestFrameworkValidationError

from rdmo.options.models import Option

from ..models import Project, Value
from ..serializers.v1 import ValueSerializer
from ..validators import ValueConflictValidator

project_id = 1
attribute_path = attribute__path='individual/single/text'
option_path = 'one_two_three/one'


def test_serializer_create(db):
    value = Value.objects.get(project_id=project_id, snapshot=None, attribute__path=attribute_path)

    class MockedRequest:
        data = {}

    class MockedView:
        request = MockedRequest()
        project = Project.objects.get(id=project_id)

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
    value = Value.objects.get(project_id=project_id, snapshot=None, attribute__path=attribute_path)

    class MockedRequest:
        data = {}

    class MockedView:
        request = MockedRequest()
        project = Project.objects.get(id=project_id)

    validator = ValueConflictValidator()
    serializer = ValueSerializer()
    serializer.context['view'] = MockedView()

    with pytest.raises(RestFrameworkValidationError):
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

    with pytest.raises(RestFrameworkValidationError):
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


def test_serializer_create_checkbox(db):
    value = Value.objects.get(
        project_id=project_id,
        snapshot=None,
        attribute__path='individual/collection/checkbox',
        collection_index=0
    )
    option = Option.objects.get(uri_path=option_path)

    class MockedRequest:
        data = {
            'widget_type': 'checkbox'
        }

    class MockedView:
        request = MockedRequest()
        project = Project.objects.get(id=project_id)

    validator = ValueConflictValidator()
    serializer = ValueSerializer()
    serializer.context['view'] = MockedView()

    validator({
        'attribute': value.attribute,
        'set_prefix': value.set_prefix,
        'set_index': value.set_index,
        'collection_index': value.collection_index,
        'option': option.id
    }, serializer)


def test_serializer_create_checkbox_error(db):
    value = Value.objects.get(
        project_id=project_id,
        snapshot=None,
        attribute__path='individual/collection/checkbox',
        collection_index=0
    )

    class MockedRequest:
        data = {
            'widget_type': 'checkbox'
        }

    class MockedView:
        request = MockedRequest()
        project = Project.objects.get(id=project_id)

    validator = ValueConflictValidator()
    serializer = ValueSerializer()
    serializer.context['view'] = MockedView()

    with pytest.raises(RestFrameworkValidationError):
        validator({
            'attribute': value.attribute,
            'set_prefix': value.set_prefix,
            'set_index': value.set_index,
            'collection_index': value.collection_index,
            'option': value.option
        }, serializer)


def test_serializer_create_checkbox_text(db):
    value = Value.objects.get(
        project_id=project_id,
        snapshot=None,
        attribute__path='individual/collection/checkbox',
        collection_index=0
    )

    class MockedRequest:
        data = {
            'widget_type': 'text'
        }

    class MockedView:
        request = MockedRequest()
        project = Project.objects.get(id=project_id)

    validator = ValueConflictValidator()
    serializer = ValueSerializer()
    serializer.context['view'] = MockedView()

    with pytest.raises(RestFrameworkValidationError):
        validator({
            'attribute': value.attribute,
            'set_prefix': value.set_prefix,
            'set_index': value.set_index,
            'collection_index': value.collection_index
        }, serializer)
