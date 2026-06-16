import pytest

from django.urls import reverse

from rdmo.core.tests.constants import multisite_status_map as status_map
from rdmo.core.tests.constants import multisite_users as users
from rdmo.questions.models import Catalog, Page, Question, QuestionSet, Section

STATUS_CODES = {
    'upload-import': {
        'foo-catalog': {
            'user': 403, 'reviewer': 403, 'editor': 200,
            'example-reviewer': 404, 'example-editor': 404, 'foo-user': 403,
            'foo-reviewer': 403, 'foo-editor': 200, 'bar-user': 403,
            'bar-reviewer': 404, 'bar-editor': 404, 'anonymous': 401,
        },
        'bar-catalog': {
            'user': 403, 'reviewer': 403, 'editor': 200,
            'example-reviewer': 404, 'example-editor': 404, 'foo-user': 403,
            'foo-reviewer': 404, 'foo-editor': 404, 'bar-user': 403,
            'bar-reviewer': 403, 'bar-editor': 200, 'anonymous': 401,
        },
        'foo-section': {
            'user': 403, 'reviewer': 403, 'editor': 200,
            'example-reviewer': 404, 'example-editor': 404, 'foo-user': 403,
            'foo-reviewer': 403, 'foo-editor': 200, 'bar-user': 403,
            'bar-reviewer': 404, 'bar-editor': 404, 'anonymous': 401,
        },
        'bar-section': {
            'user': 403, 'reviewer': 403, 'editor': 200,
            'example-reviewer': 404, 'example-editor': 404, 'foo-user': 403,
            'foo-reviewer': 404, 'foo-editor': 404, 'bar-user': 403,
            'bar-reviewer': 403, 'bar-editor': 200, 'anonymous': 401,
        },
        'foo-page': {
            'user': 403, 'reviewer': 403, 'editor': 200,
            'example-reviewer': 404, 'example-editor': 404, 'foo-user': 403,
            'foo-reviewer': 403, 'foo-editor': 200, 'bar-user': 403,
            'bar-reviewer': 404, 'bar-editor': 404, 'anonymous': 401,
        },
        'bar-page': {
            'user': 403, 'reviewer': 403, 'editor': 200,
            'example-reviewer': 404, 'example-editor': 404, 'foo-user': 403,
            'foo-reviewer': 404, 'foo-editor': 404, 'bar-user': 403,
            'bar-reviewer': 403, 'bar-editor': 200, 'anonymous': 401,
        },
        'foo-questionset': {
            'user': 403, 'reviewer': 403, 'editor': 200,
            'example-reviewer': 404, 'example-editor': 404, 'foo-user': 403,
            'foo-reviewer': 403, 'foo-editor': 200, 'bar-user': 403,
            'bar-reviewer': 404, 'bar-editor': 404, 'anonymous': 401,
        },
        'bar-questionset': {
            'user': 403, 'reviewer': 403, 'editor': 200,
            'example-reviewer': 404, 'example-editor': 404, 'foo-user': 403,
            'foo-reviewer': 404, 'foo-editor': 404, 'bar-user': 403,
            'bar-reviewer': 403, 'bar-editor': 200, 'anonymous': 401,
        },
        'foo-questionset-parent': {
            'user': 403, 'reviewer': 403, 'editor': 200,
            'example-reviewer': 404, 'example-editor': 404, 'foo-user': 403,
            'foo-reviewer': 403, 'foo-editor': 200, 'bar-user': 403,
            'bar-reviewer': 404, 'bar-editor': 404, 'anonymous': 401,
        },
        'bar-questionset-parent': {
            'user': 403, 'reviewer': 403, 'editor': 200,
            'example-reviewer': 404, 'example-editor': 404, 'foo-user': 403,
            'foo-reviewer': 404, 'foo-editor': 404, 'bar-user': 403,
            'bar-reviewer': 403, 'bar-editor': 200, 'anonymous': 401,
        },
        'foo-question': {
            'user': 403, 'reviewer': 403, 'editor': 200,
            'example-reviewer': 404, 'example-editor': 404, 'foo-user': 403,
            'foo-reviewer': 403, 'foo-editor': 200, 'bar-user': 403,
            'bar-reviewer': 404, 'bar-editor': 404, 'anonymous': 401,
        },
        'bar-question': {
            'user': 403, 'reviewer': 403, 'editor': 200,
            'example-reviewer': 404, 'example-editor': 404, 'foo-user': 403,
            'foo-reviewer': 404, 'foo-editor': 404, 'bar-user': 403,
            'bar-reviewer': 403, 'bar-editor': 200, 'anonymous': 401,
        },
    },
}

catalog_uri_paths = [
    'catalog',
    'catalog2',
    'foo-catalog',
    'bar-catalog',
]

urlnames = {
    'list': 'v1-management:import-list'
}



@pytest.mark.parametrize('username,password', users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.get(url)
    if status_map['upload-import'].get(username) == 200:
        assert response.status_code == 405, response.json()
    else:
        assert response.status_code == status_map['upload-import'].get(username), response.json()


@pytest.mark.parametrize('username,password', users)
def test_create_create(db, client, username, password, json_data, delete_all_objects):
    delete_all_objects(Catalog, Section, Page, QuestionSet, Question)

    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.post(url, json_data, content_type='application/json')

    assert response.status_code == status_map['upload-import'].get(username), response.json()

    if response.status_code == 200:
        for element in response.json():
            if any(i in username for i in ['reviewer', 'user']):
                assert element.get('created') is False
            else:
                assert element.get('created') is True
            assert element.get('updated') is False


@pytest.mark.parametrize('username,password', users)
def test_create_update(db, client, username, password, json_data):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.post(url, json_data, content_type='application/json')

    assert response.status_code == status_map['upload-import'].get(username), response.json()

    if response.status_code == 200:
        for element in response.json():
            assert element.get('created') is False
            obj_perm_status_code = STATUS_CODES['upload-import'].get(
                element['uri_path'], status_map['upload-import']
            )[username]
            if obj_perm_status_code == 200:
                assert element.get('updated') is True
            else:
                assert element.get('updated') is False


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('catalog_uri_path', catalog_uri_paths)
def test_create_update_certain_catalog(db, client, username, password, catalog_uri_path, json_data):
    client.login(username=username, password=password)

    instance_json = next(i for i in json_data['elements'] if i['uri_path'] == catalog_uri_path)
    instance_json['title_en'] += ' (updated)'
    instance_json['title_de'] += ' (updated)'
    instance_data = {'elements': [instance_json]}

    url = reverse(urlnames['list'])
    response = client.post(url, instance_data, content_type='application/json')

    assert response.status_code == status_map['upload-import'].get(username), response.json()
    if response.status_code == 200:
        obj_perm_status_code = STATUS_CODES['upload-import'].get(
            catalog_uri_path, status_map['upload-import']
        )[username]
        for element in response.json():
            assert element.get('created') is False
            if obj_perm_status_code == 200:
                assert element.get('updated') is True
            else:
                assert element.get('updated') is False


@pytest.mark.parametrize('username,password', users)
def test_create_empty(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.post(url, {}, content_type='application/json')
    if status_map['upload-import'].get(username) == 200:
        assert response.status_code == 400, response.json()
        assert 'This field may not be blank.' in response.json()['elements'], response.json()['elements']
    else:
        assert response.status_code == status_map['upload-import'].get(username), response.json()


@pytest.mark.parametrize('username,password', users)
def test_create_error(db, client, username, password):
    client.login(username=username, password=password)

    json_data = {'foo': 'bar'}

    url = reverse(urlnames['list'])
    response = client.post(url, json_data, content_type='application/json')
    if status_map['upload-import'].get(username) == 200:
        assert response.status_code == 400, response.json()
        assert 'This field may not be blank.' in response.json()['elements'], response.json()['elements']
    else:
        assert response.status_code == status_map['upload-import'].get(username), response.json()
