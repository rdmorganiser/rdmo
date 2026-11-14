import pytest

from rdmo.projects.models import Value

from ..constants import RelationTypes
from ..models import Condition


def test_condition_str(db):
    instances = Condition.objects.all()
    for instance in instances:
        assert str(instance)


def test_condition_clean(db):
    instances = Condition.objects.all()
    for instance in instances:
        instance.clean()


@pytest.mark.parametrize('relation,values', [
    (RelationTypes.RELATION_EMPTY, []),
    (RelationTypes.RELATION_NOT_EQUAL, []),
    (RelationTypes.RELATION_EQUAL, [Value(attribute=None, text='test')]),
])
def test_condition_without_source_resolves_false(relation, values):
    condition = Condition(source=None, relation=relation, target_text='test')

    assert condition.resolve(values) is False
