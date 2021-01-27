import pytest
from django.core import mail
from django.urls import reverse

from rdmo.core.constants import VALUE_TYPE_FILE

from ..models import Issue

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
    },
    'send_get': {
        'owner': 200, 'manager': 200, 'author': 200, 'guest': 403, 'user': 403, 'site': 200, 'anonymous': 302
    },
    'send_post': {
        'owner': 302, 'manager': 302, 'author': 302, 'guest': 403, 'user': 403, 'site': 302, 'anonymous': 302
    }
}

urlnames = {
    'update': 'issue_update',
    'send': 'issue_send'
}

project_pk = 1
issue_pk = 1
integration_pk = 1

issue_status = ('open', 'in_progress', 'closed')


@pytest.mark.parametrize('username,password', users)
def test_issue_update_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['update'], args=[project_pk, issue_pk])
    response = client.get(url)
    assert response.status_code == status_map['update_get'][username], response.content


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('status', issue_status)
def test_issue_update_post(db, client, username, password, status):
    client.login(username=username, password=password)

    url = reverse(urlnames['update'], args=[project_pk, issue_pk])
    data = {
        'status': status
    }
    response = client.post(url, data)
    assert response.status_code == status_map['update_post'][username], response.content
    if password and response.status_code == 302:
        assert Issue.objects.get(pk=issue_pk).status == status


@pytest.mark.parametrize('username,password', users)
def test_issue_send_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['send'], args=[project_pk, issue_pk])
    response = client.get(url)
    assert response.status_code == status_map['send_get'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_issue_send_post_email(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['send'], args=[project_pk, issue_pk])
    data = {
        'subject': 'Subject',
        'message': 'Message',
        'recipients': ['email@example.com']
    }
    response = client.post(url, data)
    assert response.status_code == status_map['send_post'][username], response.content
    if password and response.status_code == 302:
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == '[example.com] Subject'
        assert mail.outbox[0].body == 'Message'


@pytest.mark.parametrize('username,password', users)
def test_issue_send_post_attachements(db, client, files, username, password):
    client.login(username=username, password=password)

    issue = Issue.objects.get(pk=issue_pk)

    view_id = issue.project.views.first().id
    file_id = issue.project.values.filter(value_type=VALUE_TYPE_FILE).first().id

    url = reverse(urlnames['send'], args=[project_pk, issue_pk])
    data = {
        'subject': 'Subject',
        'message': 'Message',
        'recipients': 'email@example.com',
        'attachments_answers': 'project_answers',
        'attachments_views': str(view_id),
        'attachments_files': str(file_id),
        'attachments_snapshot': '',
        'attachments_format': 'html'
    }
    response = client.post(url, data)
    assert response.status_code == status_map['send_post'][username], response.content
    if password and response.status_code == 302:
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == '[example.com] Subject'
        assert mail.outbox[0].body == 'Message'

        attachments = mail.outbox[0].attachments
        assert len(attachments) == 3
        assert attachments[0][0] == 'Test.html'
        assert attachments[0][2] == 'text/html; charset=utf-8'
        assert attachments[1][0] == 'Test.html'
        assert attachments[1][2] == 'text/html; charset=utf-8'
        assert attachments[2][0] == 'test.txt'
        assert attachments[2][2] == 'text/plain'


@pytest.mark.parametrize('username,password', users)
def test_issue_send_post_integration(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['send'], args=[project_pk, issue_pk])
    data = {
        'subject': 'Subject',
        'message': 'Message',
        'integration': [1]
    }
    response = client.post(url, data)
    assert response.status_code == status_map['send_post'][username], response.content
    if password and response.status_code == 302:
        assert response.url.startswith('https://github.com')
