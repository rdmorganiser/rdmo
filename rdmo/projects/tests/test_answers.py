import pytest

from rdmo.projects.answers import AnswerTree

from ..models import Project


def iter_answer_tree_nodes(node):
    yield node
    for element in node.get('elements', ()):
        yield from iter_answer_tree_nodes(element)
    for element_set in node.get('sets', ()):
        yield from iter_answer_tree_nodes(element_set)


def test_answer_tree_preserves_collection_value_order(db):
    answer_tree = Project.objects.get(id=1).get_answer_tree()
    collection_indexes = [
        [value['collection_index'] for value in node['values']]
        for node in iter_answer_tree_nodes(answer_tree)
        if node.get('model') == 'questions.question' and len(node.get('values', ())) > 1
    ]

    assert collection_indexes
    assert all(indexes == sorted(indexes) for indexes in collection_indexes)


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
