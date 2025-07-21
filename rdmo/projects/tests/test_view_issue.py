from unittest.mock import Mock

import pytest

from django.core import mail
from django.http import HttpResponseRedirect
from django.urls import reverse

from rdmo.core.constants import VALUE_TYPE_FILE

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

view_issue_permission_map = {
    'owner': [1, 2, 3, 4, 12],
    'manager': [1, 3, 5, 12],
    'author': [1, 3, 5, 12],
    'guest': [1, 3, 5, 12],
    'user': [12],
    'api': [1, 2, 3, 4, 5, 12],
    'site': [1, 2, 3, 4, 5, 12]
}

change_issue_permission_map = delete_issue_permission_map = {
    'owner': [1, 2, 3, 4, 12],
    'manager': [1, 3],
    'author': [1, 3],
    'api': [1, 2, 3, 4, 12],
    'site': [1, 2, 3, 4, 12],
}

issues = [1, 2, 3, 4, 9]

integration_pk = 1

issue_status = ('open', 'in_progress', 'closed')

@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('issue_id', issues)
def test_issue(db, client, username, password, issue_id):
    client.login(username=username, password=password)
    issue = Issue.objects.get(id=issue_id)

    url = reverse('issue', args=[issue.project_id, issue_id])
    response = client.get(url)

    if issue.project_id in view_issue_permission_map.get(username, []):
        assert response.status_code == 200
    elif password:
        assert response.status_code == 403
    else:
        assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('issue_id', issues)
def test_issue_update_get(db, client, username, password, issue_id):
    client.login(username=username, password=password)
    issue = Issue.objects.get(id=issue_id)

    url = reverse('issue_update', args=[issue.project_id, issue_id])
    response = client.get(url)

    if issue.project_id in change_issue_permission_map.get(username, []):
        assert response.status_code == 200
    elif password:
        assert response.status_code == 403
    else:
        assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('issue_id', issues)
@pytest.mark.parametrize('status', issue_status)
def test_issue_update_post(db, client, username, password, issue_id, status):
    client.login(username=username, password=password)
    issue = Issue.objects.get(id=issue_id)

    url = reverse('issue_update', args=[issue.project_id, issue_id])
    data = {
        'status': status
    }
    response = client.post(url, data)

    if issue.project_id in change_issue_permission_map.get(username, []):
        assert response.status_code == 302
        assert Issue.objects.get(id=issue_id).status == status
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302

        assert Issue.objects.get(id=issue_id).status == issue.status



@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('issue_id', issues)
def test_issue_send_get(db, client, username, password, issue_id):
    client.login(username=username, password=password)
    issue = Issue.objects.get(id=issue_id)

    url = reverse('issue_update', args=[issue.project_id, issue_id])
    response = client.get(url)

    if issue.project_id in change_issue_permission_map.get(username, []):
        assert response.status_code == 200
    elif password:
        assert response.status_code == 403
    else:
        assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('issue_id', issues)
def test_issue_send_post_email(db, client, username, password, issue_id):
    client.login(username=username, password=password)
    issue = Issue.objects.get(id=issue_id)

    url = reverse('issue_send', args=[issue.project_id, issue_id])
    data = {
        'subject': 'Subject',
        'message': 'Message',
        'recipients': ['email@example.com']
    }
    response = client.post(url, data)

    if issue.project_id in change_issue_permission_map.get(username, []):
        assert response.status_code == 302
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == '[example.com] Subject'
        assert mail.outbox[0].body == 'Message'
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302

        assert len(mail.outbox) == 0


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('issue_id', issues)
def test_issue_send_post_attachments(db, client, files, username, password, issue_id):
    client.login(username=username, password=password)
    issue = Issue.objects.get(id=issue_id)

    view = issue.project.views.first()
    file = issue.project.values.filter(snapshot=None, value_type=VALUE_TYPE_FILE).first()

    if file and view:
        url = reverse('issue_send', args=[issue.project_id, issue_id])
        data = {
            'subject': 'Subject',
            'message': 'Message',
            'recipients': 'email@example.com',
            'attachments_answers': 'project_answers',
            'attachments_views': str(view.id),
            'attachments_files': str(file.id),
            'attachments_snapshot': '',
            'attachments_format': 'html'
        }
        response = client.post(url, data)

        if issue.project_id in change_issue_permission_map.get(username, []):
            assert response.status_code == 302
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
        else:
            if password:
                assert response.status_code == 403
            else:
                assert response.status_code == 302

            assert len(mail.outbox) == 0


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('issue_id', issues)
def test_issue_send_post_integration(db, client, mocker, username, password, issue_id):
    mocked_send_issue = Mock(return_value=HttpResponseRedirect(redirect_to='https://example.com/login/oauth/authorize'))
    mocker.patch('rdmo.projects.providers.SimpleIssueProvider.send_issue', mocked_send_issue)

    client.login(username=username, password=password)
    issue = Issue.objects.get(id=issue_id)

    url = reverse('issue_send', args=[issue.project_id, issue_id])
    data = {
        'subject': 'Subject',
        'message': 'Message',
        'integration': [integration_pk]
    }
    response = client.post(url, data)

    if issue.project_id in change_issue_permission_map.get(username, []):
        if integration_pk in Project.objects.get(pk=issue.project_id).integrations.values_list('id', flat=True):
            assert response.status_code == 302
            assert response.url.startswith('https://example.com')
        else:
            assert response.status_code == 200
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302
            assert not response.url.startswith('https://example.com')
