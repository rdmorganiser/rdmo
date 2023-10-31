import pytest

from rest_framework.exceptions import ValidationError as RestFameworkValidationError

from ..serializers.v1 import ValueSerializer
from ..validators import ValueQuotaValidator

project_id = 1
attribute_path = attribute__path='individual/single/text'


def test_serializer_create_file(db, settings):
    class MockedProject:
        file_size = 1

    class MockedView:
        action = 'create'
        project = MockedProject()

    settings.PROJECT_FILE_QUOTA = '1b'

    validator = ValueQuotaValidator()
    serializer = ValueSerializer()
    serializer.context['view'] = MockedView()

    validator({
        'value_type': 'file'
    }, serializer)


def test_serializer_create_file_error(db, settings):
    class MockedProject:
        file_size = 1

    class MockedView:
        action = 'create'
        project = MockedProject()

    settings.PROJECT_FILE_QUOTA = '0'

    validator = ValueQuotaValidator()
    serializer = ValueSerializer()
    serializer.context['view'] = MockedView()

    with pytest.raises(RestFameworkValidationError):
        validator({
            'value_type': 'file'
        }, serializer)


def test_serializer_create_text(db, settings):
    class MockedProject:
        file_size = 1

    class MockedView:
        action = 'create'
        project = MockedProject()

    settings.PROJECT_FILE_QUOTA = '0'

    validator = ValueQuotaValidator()
    serializer = ValueSerializer()
    serializer.context['view'] = MockedView()

    validator({
        'value_type': 'text'
    }, serializer)


def test_serializer_update(db, settings):
    class MockedProject:
        file_size = 1

    class MockedView:
        action = 'update'
        project = MockedProject()

    settings.PROJECT_FILE_QUOTA = '0'

    validator = ValueQuotaValidator()
    serializer = ValueSerializer()
    serializer.context['view'] = MockedView()

    validator({
        'value_type': 'file'
    }, serializer)
