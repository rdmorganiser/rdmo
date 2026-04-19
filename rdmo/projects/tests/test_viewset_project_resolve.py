import pytest

from django.urls import reverse

from ..models import Value

urlnames = {
    'resolve': 'v1-projects:project-resolve',
}

project_id = 1

@pytest.mark.parametrize('results', [
    [
        # from: http://example.com/terms/questions/catalog/conditions/set
        {'set_prefix': '', 'set_index': 0, 'element_type': 'questions', 'element_id': 104, 'result': True},
        {'set_prefix': '', 'set_index': 1, 'element_type': 'questions', 'element_id': 104, 'result': False},
    ],
    [
        # from: http://example.com/terms/questions/catalog/conditions/set_set
        {'set_prefix': '', 'set_index': 0, 'element_type': 'questionsets', 'element_id': 94, 'result': True},
        {'set_prefix': '', 'set_index': 1, 'element_type': 'questionsets', 'element_id': 94, 'result': False},
    ],
    [
        # from: http://example.com/terms/questions/catalog/conditions/set_set_question
        {'set_prefix': '', 'set_index': 0, 'element_type': 'questions', 'element_id': 127, 'result': True},
        {'set_prefix': '', 'set_index': 1, 'element_type': 'questions', 'element_id': 127, 'result': False},
    ]
])
def test_resolve_set(db, client, results):
    client.login(username='author', password='author')

    attribute_id = 114  # http://example.com/terms/domain/conditions/set/bool

    # TODO: maybe move this into the fixture
    for result in results:
        if result['result']:
            Value.objects.update_or_create(
                project_id=project_id,
                snapshot_id=None,
                attribute_id=attribute_id,
                set_prefix=result['set_prefix'],
                set_index=result['set_index'],
                defaults={
                    'text': '1'
                }
            )

    url = reverse(urlnames['resolve'], args=[project_id])
    data = [
        {k: v for k, v in result.items() if k != 'result'}
        for result in results
    ]
    response = client.post(url, data, content_type='application/json')

    assert response.status_code == 200, response.content
    for response_result, result in zip(response.json(), results, strict=True):
        assert response_result == result


@pytest.mark.parametrize('results', [
    [
        # http://example.com/terms/questions/catalog/conditions/optionset
        {'set_prefix': '', 'set_index': 0, 'element_type': 'optionsets', 'element_id': 3, 'result': True},
    ],
    [
        # http://example.com/terms/questions/catalog/conditions/optionset
        {'set_prefix': '', 'set_index': 0, 'element_type': 'optionsets', 'element_id': 3, 'result': False},
    ]
])
def test_resolve_optionset(db, client, results):
    client.login(username='author', password='author')

    attribute_id = 120  # http://example.com/terms/domain/conditions/optionset/bool

    # TODO: maybe move this into the fixture
    for result in results:
        if result['result']:
            Value.objects.update_or_create(
                project_id=project_id,
                snapshot_id=None,
                attribute_id=attribute_id,
                set_prefix=result['set_prefix'],
                set_index=result['set_index'],
                defaults={
                    'text': '1'
                }
            )

    url = reverse(urlnames['resolve'], args=[project_id])
    data = [
        {k: v for k, v in result.items() if k != 'result'}
        for result in results
    ]
    response = client.post(url, data, content_type='application/json')

    assert response.status_code == 200, response.content
    for response_result, result in zip(response.json(), results, strict=True):
        assert response_result == result
