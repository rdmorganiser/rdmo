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
        'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'api': 200, 'user': 404, 'site': 200, 'anonymous': 404
    },
    'detail': {
        'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'api': 200, 'user': 404, 'site': 200, 'anonymous': 404
    }
}

urlnames = {
    'list': 'v1-projects:project-questionset-list',
    'detail': 'v1-projects:project-questionset-detail'
}

site_id = 1
project_id = 1


@pytest.mark.parametrize('username,password', users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'], args=[project_id])
    response = client.get(url)
    assert response.status_code == status_map['list'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_detail(db, client, username, password):
    client.login(username=username, password=password)
    instances = QuestionSet.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[project_id, instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['detail'][username], response.json()
