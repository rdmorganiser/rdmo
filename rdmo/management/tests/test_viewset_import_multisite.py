import pytest

from django.urls import reverse

from rdmo.core.tests.constants import multisite_users as users
from rdmo.core.tests.utils import get_obj_perms_status_code
from rdmo.questions.models import Catalog, Page, Question, QuestionSet, Section

status_map = {
    'list': {
        'default': 405, 'anonymous': 401
    },
    'create': {
        'default': 200, 'anonymous': 401
    },
    'create_error': {
        'default': 400, 'anonymous': 401
    }
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
    assert response.status_code == status_map['list'].get(username, status_map['list']['default']), response.json()


@pytest.mark.parametrize('username,password', users)
def test_create_create(db, client, username, password, json_data, delete_all):
    delete_all(Catalog, Section, Page, QuestionSet, Question)

    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.post(url, json_data, content_type='application/json')

    assert response.status_code == status_map['create'].get(username, status_map['create']['default']), response.json()

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

    assert response.status_code == status_map['create'].get(username, status_map['create']['default']), response.json()

    if response.status_code == 200:
        for element in response.json():
            assert element.get('created') is False
            obj_perm_status_code = get_obj_perms_status_code(element.get('uri_path'), username, 'update')
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

    assert response.status_code == status_map['create'].get(username, status_map['create']['default']), response.json()
    if response.status_code == 200:
        obj_perm_status_code = get_obj_perms_status_code(catalog_uri_path, username, 'update')
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
    assert response.status_code == status_map['create_error'].get(username, status_map['create_error']['default']), \
           response.json()


@pytest.mark.parametrize('username,password', users)
def test_create_error(db, client, username, password):
    client.login(username=username, password=password)

    json_data = {'foo': 'bar'}

    url = reverse(urlnames['list'])
    response = client.post(url, json_data, content_type='application/json')
    assert response.status_code == status_map['create_error'].get(username, status_map['create_error']['default']), \
           response.json()
