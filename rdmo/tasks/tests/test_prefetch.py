import pytest

from ..serializers.export import TaskExportSerializer
from ..viewsets import TaskViewSet
from .helpers import create_tasks_with_conditions


@pytest.mark.performance
@pytest.mark.parametrize('action,task_count', [
    ('export', 1),
    ('export', 4),
    ('detail_export', 1),
])
def test_task_export_prefetch(
    db, django_assert_num_queries, action, task_count
):
    created_tasks, attributes, conditions = create_tasks_with_conditions(
        task_count, 'query-safety-task-export'
    )
    task_ids = [task.pk for task in created_tasks]
    expected_conditions = [
        (condition.uri, condition.source.uri, condition.target_option.uri)
        for condition in conditions
    ]

    view = TaskViewSet()
    view.action = action

    # Reload through the production queryset, without setup-object caches.
    with django_assert_num_queries(3):
        tasks = list(view.get_queryset().filter(pk__in=task_ids))

    # Bulk ancestor-map queries only, without per-task attribute lookups.
    with django_assert_num_queries(2):
        context = view.get_export_serializer_context(tasks)

    assert set(context['attribute_map']) == {
        attribute.pk for attribute in attributes.values()
    }

    with django_assert_num_queries(0):
        data = TaskExportSerializer(tasks, many=True, context=context).data

    assert [item['uri'] for item in data] == [
        task.uri for task in created_tasks
    ]
    for item in data:
        assert item['start_attribute']['uri'] == attributes['start'].uri
        assert item['end_attribute']['uri'] == attributes['end'].uri
        assert item['catalogs'] == []
        assert [
            (
                condition['uri'],
                condition['source']['uri'],
                condition['target_option']['uri'],
            )
            for condition in item['conditions']
        ] == expected_conditions
