import pytest

from django.urls import reverse

from rdmo.questions.models import Catalog, Page, Question, QuestionSet, Section

users = (
    ('editor', 'editor'),
    ('reviewer', 'reviewer'),
    ('user', 'user'),
    ('api', 'api'),
    ('anonymous', None),
)

status_map = {
    'list': {
        'editor': 405, 'reviewer': 405, 'api': 405, 'user': 405, 'anonymous': 401
    },
    'create': {
        'editor': 200, 'reviewer': 200, 'api': 200, 'user': 200, 'anonymous': 401
    },
    'create_error': {
        'editor': 400, 'reviewer': 400, 'api': 400, 'user': 400, 'anonymous': 401
    }
}

urlnames = {
    'list': 'v1-management:import-list'
}


@pytest.mark.parametrize('username,password', users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.get(url)
    assert response.status_code == status_map['list'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_create_create(db, client, username, password, json_data, delete_all_objects):
    delete_all_objects(Catalog, Section, Page, QuestionSet, Question)

    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.post(url, json_data, content_type='application/json')

    assert response.status_code == status_map['create'][username], response.json()
    if response.status_code == 200:
        for element in response.json():
            if username in ['reviewer', 'user']:
                assert element.get('created') is False
            else:
                assert element.get('created') is True
            assert element.get('updated') is False


@pytest.mark.parametrize('username,password', users)
def test_create_update(db, client, username, password, json_data):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.post(url, json_data, content_type='application/json')

    assert response.status_code == status_map['create'][username], response.json()
    if response.status_code == 200:
        for element in response.json():
            assert element.get('created') is False
            assert element.get('updated') is False if username in ['reviewer', 'user'] else True


@pytest.mark.parametrize('username,password', users)
def test_create_empty(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.post(url, {}, content_type='application/json')
    assert response.status_code == status_map['create_error'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_create_error(db, client, username, password):
    client.login(username=username, password=password)

    json_data = {'foo': 'bar'}

    url = reverse(urlnames['list'])
    response = client.post(url, json_data, content_type='application/json')
    assert response.status_code == status_map['create_error'][username], response.json()
