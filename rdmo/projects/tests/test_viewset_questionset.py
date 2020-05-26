import pytest
from django.urls import reverse
from rdmo.questions.models import QuestionSet

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

status_map = {
    'list': {
        'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'api': 200, 'user': 200, 'site': 200, 'anonymous': 401
    },
    'detail': {
        'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'api': 200, 'user': 200, 'site': 200, 'anonymous': 401
    }
}

urlnames = {
    'list': 'v1-projects:questionset-list',
    'detail': 'v1-projects:questionset-detail',
    'first': 'v1-projects:questionset-first',
    'prev': 'v1-projects:questionset-prev',
    'next': 'v1-projects:questionset-next'
}

catalog_pk = 1
catalog_pk_wrong = 2


@pytest.mark.parametrize('username,password', users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.get(url)
    assert response.status_code == status_map['list'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_detail(db, client, username, password):
    client.login(username=username, password=password)
    instances = QuestionSet.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['detail'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_first(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['first']) + '?catalog={}'.format(catalog_pk)
    response = client.get(url)
    assert response.status_code == status_map['list'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_first_error(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['first'])
    response = client.get(url)
    assert response.status_code == (401 if username == 'anonymous' else 404), response.json()


@pytest.mark.parametrize('username,password', users)
def test_prev(db, client, username, password):
    client.login(username=username, password=password)
    instances = QuestionSet.objects.order_by_catalog(catalog_pk)

    for i, instance in enumerate(instances):
        url = reverse(urlnames['prev'], args=[instance.pk])
        response = client.get(url)

        if i == 0:
            assert response.status_code == (401 if username == 'anonymous' else 404), response.json()
        else:
            assert response.status_code == status_map['detail'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_next(db, client, username, password):
    client.login(username=username, password=password)
    instances = QuestionSet.objects.order_by_catalog(catalog_pk)

    for i, instance in enumerate(instances):
        url = reverse(urlnames['next'], args=[instance.pk])
        response = client.get(url)

        if i == len(instances) - 1:
            assert response.status_code == (401 if username == 'anonymous' else 404), response.json()
        else:
            assert response.status_code == status_map['detail'][username], response.json()
