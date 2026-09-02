import pytest

from rdmo.projects.answers import AnswerTree

from ..models import Project


def test_conditions_fallback(db):
    project = Project.objects.get(id=1)
    answer_tree = AnswerTree(project.catalog, project.values.filter(snapshot=None))

    assert set(answer_tree.conditions) == set(project.catalog.conditions.values_list('id', flat=True))


def test_for_answer_tree_orders_values_and_loads_required_fields(db):
    values = Project.objects.get(id=1).values.filter(snapshot=None)
    answer_tree_values = list(values.for_answer_tree())

    sort_keys = [
        (value.attribute_id, value.set_prefix, value.set_index, value.collection_index)
        for value in answer_tree_values
    ]
    assert sort_keys == sorted(sort_keys)
    assert not {
        'project_id', 'snapshot_id', 'attribute_id', 'set_prefix', 'set_index', 'set_collection', 'collection_index',
        'text', 'option_id', 'file', 'external_id',
    }.intersection(answer_tree_values[0].get_deferred_fields())


def test_conditions_prefetch(db, django_assert_num_queries):
    project = Project.objects.get(id=1)
    project.catalog.prefetch_elements()
    condition_ids = set(project.catalog.conditions.values_list('id', flat=True))

    with django_assert_num_queries(0):
        answer_tree = AnswerTree(project.catalog, ())

    assert set(answer_tree.conditions) == condition_ids


@pytest.mark.parametrize('parent_set, set_level', [
    (None, 0),
    (('0', 0), 1),
    (('1|2', 1), 2),
    (('3|4|5', 2), 3),
    (('6|7|8|9', 3), 4),
])
def test_compute_set_level(parent_set, set_level):
    assert AnswerTree.compute_set_level(parent_set) == set_level


@pytest.mark.parametrize('parent_set, set_prefix', [
    (None, ''),
    (('', 0), '0'),
    (('0', 1), '0|1'),
    (('1|2', 3), '1|2|3'),
    (('4|5|6', 7), '4|5|6|7')
])
def test_compute_child_set_prefix(parent_set, set_prefix):
    assert AnswerTree.compute_child_set_prefix(parent_set) == set_prefix


@pytest.mark.parametrize('descendant_set_prefix, level, ancestor_set', [
    (None, 1, None),
    ('', 1, None),
    ('1|2|3|4|5', 1, ('1', 2)),
    ('1|2|3|4|5', 2, ('1|2', 3)),
    ('1|2|3|4|5', 3, ('1|2|3', 4)),
    ('1|2|3|4|5', 4, ('1|2|3|4', 5)),
    ('1|2|3|4|5', 5, None)
])
def test_compute_ancestor_set(descendant_set_prefix, level, ancestor_set):
    assert AnswerTree.compute_ancestor_set(descendant_set_prefix, level) == ancestor_set
