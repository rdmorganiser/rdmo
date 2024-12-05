import pytest

from django.urls import reverse

users = (
    ('owner', 'owner'),
    ('manager', 'manager'),
    ('author', 'author'),
    ('guest', 'guest'),
    ('api', 'api'),
    ('user', 'user'),
    ('site', 'site'),
    ('anonymous', None),
)

view_questionset_permission_map = {
    'owner': [1, 2, 3, 4, 5],
    'manager': [1, 3, 5],
    'author': [1, 3, 5],
    'guest': [1, 3, 5],
    'api': [1, 2, 3, 4, 5],
    'site': [1, 2, 3, 4, 5]
}

urlnames = {
    'list': 'v1-projects:project-page-list',
    'detail': 'v1-projects:project-page-detail'
}

projects = [1, 2, 3, 4, 5]
pages = [1]


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('page_id', pages)
def test_detail(db, client, username, password, project_id, page_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['detail'], args=[project_id, page_id])
    response = client.get(url)

    if project_id in view_questionset_permission_map.get(username, []):
        assert response.status_code == 200
        assert response.json().get('id') == page_id
    else:
        assert response.status_code == 404


def test_detail_order_in_page(db, client):
    project_id = 1
    username = 'owner'
    ordered_page = 16
    ordered_page_question_ids = {
        16: [18, 19, 32, 33, 34, 89, 35, 36, 82]
    }

    client.login(username=username, password=username)

    url = reverse(urlnames['detail'], args=[project_id, ordered_page])
    response = client.get(url)

    data = response.json()
    questions = [i for i in data['elements'] if i['model'] == "questions.question"]
    question_ids = [i['id'] for i in questions]

    assert response.status_code == 200
    assert response.json().get('id') == ordered_page
    assert question_ids == ordered_page_question_ids.get(ordered_page)


def test_detail_page_with_nested_questionsets(db, client):
    project_id = 1
    username = 'owner'
    page_id = 87
    nested_questionsets_id = [90]
    nested_element_ids = [95, 96, 94, 89]

    client.login(username=username, password=username)

    url = reverse(urlnames['detail'], args=[project_id, page_id])
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    questionsets = [i for i in data['elements'] if i['model'] == "questions.questionset"]
    questionsets_ids = [i['id'] for i in questionsets]
    assert questionsets_ids == nested_questionsets_id
    element_ids = [i['id'] for qs in questionsets for i in qs['elements']]
    assert element_ids == nested_element_ids


@pytest.mark.parametrize('direction', ['next', 'prev'])
def test_detail_page_resolve_next_relevant_page(db, client, direction):
    project_id = 1
    username = 'owner'
    start_page_id = 64
    end_page_id = 69

    client.login(username=username, password=username)

    if direction == 'next':
        next_page_id = start_page_id + 1
        add_url = ''
    else:  # direction == 'prev':
        start_page_id, end_page_id = end_page_id, start_page_id
        next_page_id = start_page_id - 1
        add_url = '?back=true'

    # get the starting page
    url = reverse(urlnames['detail'], args=[project_id, start_page_id])
    response = client.get(f'{url}{add_url}')
    assert response.status_code == 200
    assert response.json().get(f'{direction}_page') == next_page_id

    # get the following page, depending on direction
    url_next = reverse(urlnames['detail'], args=[project_id, next_page_id])
    response_next = client.get(f'{url_next}{add_url}')
    assert response_next.status_code == 303

    # this should show the redirect to the next relevant page
    assert response_next.url.endswith(f'{end_page_id}/')

    # a get on the redirected url as a double check
    response_next_relevant = client.get(response_next.url)
    assert response_next_relevant.status_code == 200
