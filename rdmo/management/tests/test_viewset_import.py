import json

from pathlib import Path

import pytest
from django.conf import settings
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
        'editor': 405, 'reviewer': 403, 'api': 405, 'user': 403, 'anonymous': 401
    },
    'create': {
        'editor': 200, 'reviewer': 403, 'api': 200, 'user': 403, 'anonymous': 401
    },
    'create_error': {
        'editor': 400, 'reviewer': 403, 'api': 400, 'user': 403, 'anonymous': 401
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
def test_create_create(db, client, username, password):
    Catalog.objects.all().delete()
    Section.objects.all().delete()
    Page.objects.all().delete()
    QuestionSet.objects.all().delete()
    Question.objects.all().delete()

    client.login(username=username, password=password)

    json_file = Path(settings.BASE_DIR) / 'import' / 'catalogs.json'
    json_data = {
        'elements': json.loads(json_file.read_text())
    }

    url = reverse(urlnames['list'])
    response = client.post(url, json_data, content_type='application/json')

    assert response.status_code == status_map['create'][username], response.json()
    if response.status_code == 200:
        for element in response.json():
            assert element.get('created') is True
            assert element.get('updated') is False


@pytest.mark.parametrize('username,password', users)
def test_create_update(db, client, username, password):
    client.login(username=username, password=password)

    json_file = Path(settings.BASE_DIR) / 'import' / 'catalogs.json'
    json_data = {
        'elements': json.loads(json_file.read_text())
    }

    url = reverse(urlnames['list'])
    response = client.post(url, json_data, content_type='application/json')

    assert response.status_code == status_map['create'][username], response.json()
    if response.status_code == 200:
        for element in response.json():
            assert element.get('created') is False
            assert element.get('updated') is True


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
