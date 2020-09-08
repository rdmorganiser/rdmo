import pytest
from django.urls import reverse

from ..models import Issue, Project

users = (
    ('owner', 'owner'),
    ('manager', 'manager'),
    ('author', 'author'),
    ('guest', 'guest'),
    ('user', 'user'),
    ('site', 'site'),
    ('anonymous', None),
)

status_map = {
    'update_get': {
        'owner': 200, 'manager': 200, 'author': 200, 'guest': 403, 'user': 403, 'site': 200, 'anonymous': 302
    },
    'update_post': {
        'owner': 302, 'manager': 302, 'author': 302, 'guest': 403, 'user': 403, 'site': 302, 'anonymous': 302
    }
}

urlnames = {
    'update': 'issue_update',
}

project_pk = 1
issue_pk = 1

issue_status = ('open', 'in_progress', 'closed')


@pytest.mark.parametrize('username,password', users)
def test_membership_update_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['update'], args=[project_pk, issue_pk])
    response = client.get(url)
    assert response.status_code == status_map['update_get'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_membership_update_post(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['update'], args=[project_pk, issue_pk])
    for status in issue_status:
        data = {
            'status': status
        }
        response = client.post(url, data)
        assert response.status_code == status_map['update_post'][username], response.content
