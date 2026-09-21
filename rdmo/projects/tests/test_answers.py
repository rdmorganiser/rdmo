import pytest

from rdmo.conditions.models import Condition
from rdmo.projects.answers import AnswerTree
from rdmo.questions.models import Page, Question, QuestionSet

from ..models import Project


def iter_answer_tree_nodes(node):
    yield node
    for element in node.get('elements', ()):
        yield from iter_answer_tree_nodes(element)
    for element_set in node.get('sets', ()):
        yield from iter_answer_tree_nodes(element_set)


@pytest.mark.parametrize('verbose', [(), ('value',)])
@pytest.mark.parametrize('snapshot_id', [None, 1])
def test_answer_tree_preserves_collection_value_order(db, verbose, snapshot_id):
    project = Project.objects.get(id=1)
    snapshot = project.snapshots.get(pk=snapshot_id) if snapshot_id else None
    answer_tree = project.get_answer_tree(snapshot=snapshot, verbose=verbose)
    collection_indexes = [
        [value['collection_index'] for value in node['values']]
        for node in iter_answer_tree_nodes(answer_tree)
        if node.get('model') == 'questions.question' and len(node.get('values', ())) > 1
    ]

    assert collection_indexes
    assert all(indexes == sorted(indexes) for indexes in collection_indexes)

    if 'value' in verbose:
        value_ids = {
            value['id']
            for node in iter_answer_tree_nodes(answer_tree)
            for value in node.get('values', ())
            if value['id'] is not None
        }
        assert value_ids
        assert value_ids <= set(project.values.filter(snapshot=snapshot).values_list('id', flat=True))


@pytest.mark.parametrize('verbose', [(), ('value',)])
def test_preloaded_answer_tree_needs_no_queries(db, django_assert_num_queries, verbose):
    project = Project.objects.select_related('catalog').get(pk=1)
    project.catalog.prefetch_elements()
    values = project.values.filter(snapshot=None).order_by(
        'attribute_id', 'set_prefix', 'set_index', 'collection_index'
    )
    if 'value' in verbose:
        values = values.select_related('option')
    values = list(values)

    # Include construction and the first traversal; do not warm model cached properties.
    with django_assert_num_queries(0):
        answer_tree = AnswerTree(project.catalog, values, verbose=verbose).compute()

    assert answer_tree['id'] == project.catalog_id
    assert answer_tree['elements']


def test_answer_tree_consumes_values_once(db, mocker):
    project = Project.objects.select_related('catalog').get(pk=1)
    project.catalog.prefetch_elements()
    queryset = project.values.filter(snapshot=None).order_by(
        'attribute_id', 'set_prefix', 'set_index', 'collection_index'
    )
    values = mocker.MagicMock()
    values.__iter__.side_effect = lambda: iter(queryset)

    answer_tree = AnswerTree(project.catalog, values).compute()

    assert answer_tree['elements']
    assert values.__iter__.call_count == 1


def test_answer_tree_resolves_empty_conditions(db):
    question = Question.objects.get(uri='http://example.com/terms/questions/catalog/individual/text/text')
    question.conditions.clear()
    answer_tree = AnswerTree(catalog=None, values=[])

    assert answer_tree.resolve_conditions(question, ('', 0)) is True


def test_answer_tree_reuses_condition_result(db, mocker):
    project = Project.objects.get(pk=1)
    template = Condition.objects.get(uri='http://example.com/terms/conditions/text_equal_test')
    condition = Condition.objects.create(
        uri_prefix=template.uri_prefix,
        uri_path='answer-tree-cache-test',
        source_id=template.source_id,
        relation=template.relation,
        target_text=template.target_text,
    )
    questions = list(Question.objects.filter(uri__in=(
        'http://example.com/terms/questions/catalog/individual/text/text',
        'http://example.com/terms/questions/catalog/individual/textarea/textarea',
    )))
    assert len(questions) == 2
    for question in questions:
        question.conditions.set([condition])

    project.catalog.prefetch_elements()
    resolve_spy = mocker.spy(Condition, 'resolve')
    answer_tree = project.get_answer_tree()
    question_nodes = {
        node['id']: node
        for node in iter_answer_tree_nodes(answer_tree)
        if node.get('model') == 'questions.question'
    }

    assert all(question_nodes[question.id]['show'] for question in questions)
    assert sum(call.args[0].pk == condition.pk for call in resolve_spy.call_args_list) == 1


@pytest.mark.parametrize('condition_uris,show', [
    ((), True),
    (('http://example.com/terms/conditions/text_not_equal_test',), False),
    ((
        'http://example.com/terms/conditions/text_not_equal_test',
        'http://example.com/terms/conditions/text_equal_test',
    ), True),
])
def test_answer_tree_condition_visibility(db, condition_uris, show):
    project = Project.objects.get(pk=1)
    question = Question.objects.get(uri='http://example.com/terms/questions/catalog/individual/text/text')
    question.conditions.set(Condition.objects.filter(uri__in=condition_uris))

    project.catalog.prefetch_elements()
    answer_tree = project.get_answer_tree()
    node = next(node for node in iter_answer_tree_nodes(answer_tree)
                if node.get('model') == 'questions.question' and node['id'] == question.id)

    assert node['show'] is show
    if show:
        assert (node['count'], node['total']) == (1, 1)
    else:
        assert (node['count'], node['total']) == (0, 0)
        assert 'values' not in node


@pytest.mark.parametrize('question_uri,answered,count,total', [
    ('http://example.com/terms/questions/catalog/blocks/optional/block/mandatory', False, 0, 1),
    ('http://example.com/terms/questions/catalog/blocks/optional/block/mandatory', True, 1, 1),
    ('http://example.com/terms/questions/catalog/blocks/optional/block/optional', False, 0, 0),
    ('http://example.com/terms/questions/catalog/blocks/optional/block/optional', True, 1, 1),
])
def test_answer_tree_question_progress(db, question_uri, answered, count, total):
    project = Project.objects.get(pk=1)
    question = Question.objects.get(uri=question_uri)
    if answered:
        project.values.update_or_create(
            snapshot=None, attribute_id=question.attribute_id,
            set_prefix='0', set_index=0, collection_index=0,
            defaults={'text': 'answer'},
        )

    project.catalog.prefetch_elements()
    answer_tree = project.get_answer_tree()
    node = next(node for node in iter_answer_tree_nodes(answer_tree)
                if node.get('model') == 'questions.question' and node['id'] == question.id)

    assert (node['count'], node['total']) == (count, total)
    assert node['is_empty'] is not answered
    assert len(node['values']) == 1
    assert node['values'][0]['is_empty'] is not answered


@pytest.mark.parametrize('parent_index,child_indexes,nested_indexes', [
    (1, [0, 1, 2], [0, 1, 2]),
    (10, [2, 4], [3]),
])
def test_answer_tree_nested_collection_sets(db, parent_index, child_indexes, nested_indexes):
    project = Project.objects.get(pk=1)
    for question_uri, set_prefix, set_index in (
        ('http://example.com/terms/questions/catalog/blocks/set/block/a', '10', 4),
        ('http://example.com/terms/questions/catalog/blocks/set/block/block/y', '10|2', 3),
    ):
        question = Question.objects.get(uri=question_uri)
        project.values.update_or_create(
            snapshot=None, attribute_id=question.attribute_id,
            set_prefix=set_prefix, set_index=set_index, collection_index=0,
            defaults={'text': 'answer'},
        )

    project.catalog.prefetch_elements()
    answer_tree = project.get_answer_tree()
    page_element = Page.objects.get(uri='http://example.com/terms/questions/catalog/blocks/set')
    questionset_element = QuestionSet.objects.get(uri='http://example.com/terms/questions/catalog/blocks/set/block')
    nested_questionset_element = QuestionSet.objects.get(
        uri='http://example.com/terms/questions/catalog/blocks/set/block/block'
    )
    page = next(node for node in iter_answer_tree_nodes(answer_tree)
                if node.get('model') == 'questions.page' and node['id'] == page_element.id)
    parent_set = next(node for node in page['sets'] if node['set_index'] == parent_index)
    questionset = next(node for node in parent_set['elements']
                       if node['model'] == 'questions.questionset' and node['id'] == questionset_element.id)

    assert [(node['set_prefix'], node['set_index']) for node in questionset['sets']] == [
        (str(parent_index), index) for index in child_indexes
    ]

    child_set = next(node for node in questionset['sets'] if node['set_index'] == 2)
    nested_questionset = next(node for node in child_set['elements']
                              if node['model'] == 'questions.questionset'
                              and node['id'] == nested_questionset_element.id)
    assert [(node['set_prefix'], node['set_index']) for node in nested_questionset['sets']] == [
        (f'{parent_index}|2', index) for index in nested_indexes
    ]


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
