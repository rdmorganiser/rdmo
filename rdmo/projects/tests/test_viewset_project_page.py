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
    username = 'user'
    ordered_page = 16
    ordered_page_question_ids = {
        16: [18, 19, 32, 33, 34, 89, 35, 36, 82]
    }

    client.login(username=username, password=username)

    url = reverse(urlnames['detail'], args=[project_id, ordered_page])
    response = client.get(url)

    if project_id in view_questionset_permission_map.get(username, []):
        data = response.json()
        questions = [i for i in data['elements'] if i['model'] == "questions.question"]
        question_ids = [i['id'] for i in questions]

        assert response.status_code == 200
        assert response.json().get('id') == ordered_page
        assert question_ids == ordered_page_question_ids.get(ordered_page)
    else:
        assert response.status_code == 404
