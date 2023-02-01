import pytest

from rdmo.conditions.models import Condition

from ..models import Project, Value

project_id = 1
value_id = 86
set_indexes = (0, 1)


@pytest.mark.parametrize('set_index', set_indexes)
def test_set_collection(db, set_index):
    # test the special case, when a condition of a question in a set is checked
    # and the value for the conditions source was not entered as part of as set
    condition = Condition.objects.get(uri='http://example.com/terms/conditions/text_contains_test')
    values = Project.objects.get(id=project_id).values.filter(snapshot=None)

    result = condition.resolve(values, set_index=set_index)
    assert result is True


@pytest.mark.parametrize('set_index', set_indexes)
def test_set_collection_error_none(db, set_index):
    # same as test_set_collection, but with set_collection = True
    value = Value.objects.get(id=value_id)
    value.set_collection = True
    value.save()

    condition = Condition.objects.get(uri='http://example.com/terms/conditions/text_contains_test')
    values = Project.objects.get(id=project_id).values.filter(snapshot=None)
    result = condition.resolve(values, set_index=set_index)
    assert result is (True if set_index == 0 else False)


@pytest.mark.parametrize('set_index', set_indexes)
def test_set_collection_error_true(db, set_index):
    # same as test_set_collection, but with set_collection = None
    value = Value.objects.get(id=value_id)
    value.set_collection = None
    value.save()

    condition = Condition.objects.get(uri='http://example.com/terms/conditions/text_contains_test')
    values = Project.objects.get(id=project_id).values.filter(snapshot=None)
    result = condition.resolve(values, set_index=set_index)
    assert result is (True if set_index == 0 else False)
