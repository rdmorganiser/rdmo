import pytest

from django.core import mail
from django.http import HttpResponseRedirect
from django.urls import reverse

from rdmo.core.constants import VALUE_TYPE_FILE

from ..models import Issue

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

view_issue_permission_map = {
    'owner': [1, 2, 3, 4, 5, 12],
    'manager': [1, 3, 5, 12],
    'author': [1, 3, 5, 12],
    'guest': [1, 3, 5, 12],
    'user': [12],
    'api': [1, 2, 3, 4, 5, 12],
    'site': [1, 2, 3, 4, 5, 12]
}

add_issue_permission_map = delete_issue_permission_map = {
    'owner': [1, 2, 3, 4, 5, 12],
    'manager': [1, 3, 5],
    'api': [1, 2, 3, 4, 5, 12],
    'site': [1, 2, 3, 4, 5, 12]
}

change_issue_permission_map = {
    'owner': [1, 2, 3, 4, 5, 12],
    'manager': [1, 3, 5],
    'author': [1, 3, 5],
    'api': [1, 2, 3, 4, 5, 12],
    'site': [1, 2, 3, 4, 5, 12]
}

urlnames = {
    'list': 'v1-projects:project-issue-list',
    'detail': 'v1-projects:project-issue-detail',
    'send-email': 'v1-projects:project-issue-send-email',
    'send-integration': 'v1-projects:project-issue-send-integration'
}

projects = [1, 2, 3, 4, 5, 12]
issues = [1, 2, 3, 4, 9]
issues_visible = [8, 9]

issue_status = ('open', 'in_progress', 'closed')


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_list(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'], args=[project_id])
    response = client.get(url)

    if project_id in view_issue_permission_map.get(username, []):
        assert response.status_code == 200

        response_items = response.json()
        if username == 'user':
            assert sorted([item['id'] for item in response_items]) == issues_visible
        else:
            values_list = Issue.objects.filter(project_id=project_id) \
                                       .order_by('id').values_list('id', flat=True)
            assert sorted([item['id'] for item in response_items]) == list(values_list)

        assert all(isinstance(item['resolve'], bool) for item in response_items)
        assert all(isinstance(item['dates'], list) for item in response_items)
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('issue_id', issues)
def test_detail(db, client, username, password, issue_id):
    client.login(username=username, password=password)
    issue = Issue.objects.get(id=issue_id)

    url = reverse(urlnames['detail'], args=[issue.project_id, issue_id])
    response = client.get(url)

    if issue.project_id in view_issue_permission_map.get(username, []):
        assert response.status_code == 200
        response_data = response.json()
        assert isinstance(response_data, dict)
        assert response_data['id'] == issue_id
        assert isinstance(response_data['resolve'], bool)
        assert isinstance(response_data['dates'], list)
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_create(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'], args=[project_id])
    response = client.post(url)

    if project_id in add_issue_permission_map.get(username, []):
        assert response.status_code == 405
    elif project_id in view_issue_permission_map.get(username, []):
        assert response.status_code == 403
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('issue_id', issues)
@pytest.mark.parametrize('status', issue_status)
def test_update(db, client, username, password, issue_id, status):
    client.login(username=username, password=password)
    issue = Issue.objects.get(id=issue_id)

    url = reverse(urlnames['detail'], args=[issue.project_id, issue_id])
    data = {
        'status': status
    }
    response = client.put(url, data, content_type='application/json')

    if issue.project_id in change_issue_permission_map.get(username, []):
        assert response.status_code == 200
        assert response.json().get('status') == status
    elif issue.project_id in view_issue_permission_map.get(username, []):
        assert response.status_code == 403
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('issue_id', issues)
def test_delete(db, client, username, password, issue_id):
    client.login(username=username, password=password)
    issue = Issue.objects.get(id=issue_id)

    url = reverse(urlnames['detail'], args=[issue.project_id, issue_id])
    response = client.delete(url)

    if issue.project_id in delete_issue_permission_map.get(username, []):
        assert response.status_code == 405
    elif issue.project_id in view_issue_permission_map.get(username, []):
        assert response.status_code == 405
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
def test_send_email(db, client, settings, username, password):
    client.login(username=username, password=password)
    issue = Issue.objects.get(pk=1)

    url = reverse(urlnames['send-email'], args=[issue.project_id, issue.id])
    data = {
        'subject': 'Subject',
        'message': 'Message',
        'recipients': [settings.EMAIL_RECIPIENTS_CHOICES[0][0]]
    }
    response = client.post(url, data, content_type='application/json')

    if issue.project_id in change_issue_permission_map.get(username, []):
        assert response.status_code == 204
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == '[example.com] Subject'
        assert mail.outbox[0].body == 'Message'
        assert mail.outbox[0].to == ['email@example.com']
        assert mail.outbox[0].cc == [f'{username}@example.com']
        assert mail.outbox[0].reply_to == [f'{username}@example.com']

        issue.refresh_from_db()
        assert issue.status == Issue.ISSUE_STATUS_IN_PROGRESS
    else:
        if issue.project_id in view_issue_permission_map.get(username, []):
            assert response.status_code == 403
        else:
            assert response.status_code == 404

        assert len(mail.outbox) == 0
        issue.refresh_from_db()
        assert issue.status == Issue.ISSUE_STATUS_OPEN


def test_send_email_attachments(db, client, settings, files):
    client.login(username='owner', password='owner')
    issue = Issue.objects.get(pk=1)
    view = issue.project.views.first()
    file = issue.project.values.filter(snapshot=None, value_type=VALUE_TYPE_FILE).first()

    url = reverse(urlnames['send-email'], args=[issue.project_id, issue.id])
    data = {
        'subject': 'Subject',
        'message': 'Message',
        'recipients': [settings.EMAIL_RECIPIENTS_CHOICES[0][0]],
        'attachments_answers': ['project_answers'],
        'attachments_views': [view.id],
        'attachments_files': [file.id],
        'attachments_snapshot': 'current',
        'attachments_format': 'html'
    }
    response = client.post(url, data, content_type='application/json')

    assert response.status_code == 204
    assert len(mail.outbox) == 1

    attachments = mail.outbox[0].attachments
    assert len(attachments) == 3
    assert attachments[0][0] == 'Test.html'
    assert attachments[0][2] == 'text/html; charset=utf-8'
    assert attachments[1][0] == 'Test.html'
    assert attachments[1][2] == 'text/html; charset=utf-8'
    assert attachments[2][0] == 'test.txt'
    assert attachments[2][2] == 'text/plain'


def test_send_email_snapshot_file(db, client, settings, files):
    client.login(username='owner', password='owner')
    issue = Issue.objects.get(pk=1)
    snapshot = issue.project.snapshots.get(pk=7)
    file = issue.project.values.filter(snapshot=snapshot, value_type=VALUE_TYPE_FILE).first()

    url = reverse(urlnames['send-email'], args=[issue.project_id, issue.id])
    data = {
        'subject': 'Subject',
        'message': 'Message',
        'recipients': [settings.EMAIL_RECIPIENTS_CHOICES[0][0]],
        'attachments_files': [file.id],
        'attachments_snapshot': snapshot.id
    }
    response = client.post(url, data, content_type='application/json')

    assert response.status_code == 204
    assert len(mail.outbox) == 1
    assert len(mail.outbox[0].attachments) == 1
    assert mail.outbox[0].attachments[0][0] == 'test.txt'
    assert mail.outbox[0].attachments[0][2] == 'text/plain'


@pytest.mark.parametrize('data,error_field', [
    ({}, 'recipients'),
    ({'attachments_answers': ['project_answers']}, 'attachments_format'),
    ({'attachments_views': [2], 'attachments_format': 'html'}, 'attachments_views'),
    ({'attachments_files': [338], 'attachments_snapshot': 'current'}, 'attachments_files')
])
def test_send_email_error(db, client, settings, data, error_field):
    client.login(username='owner', password='owner')
    issue = Issue.objects.get(pk=1)

    url = reverse(urlnames['send-email'], args=[issue.project_id, issue.id])
    request_data = {
        'subject': 'Subject',
        'message': 'Message',
        'recipients': [settings.EMAIL_RECIPIENTS_CHOICES[0][0]],
        **data
    }
    if error_field == 'recipients':
        request_data['recipients'] = []

    response = client.post(url, request_data, content_type='application/json')

    assert response.status_code == 400
    assert error_field in response.json()
    assert len(mail.outbox) == 0


def test_send_email_disabled(db, client, settings):
    settings.PROJECT_SEND_ISSUE = False
    client.login(username='owner', password='owner')
    issue = Issue.objects.get(pk=1)

    url = reverse(urlnames['send-email'], args=[issue.project_id, issue.id])
    response = client.post(url, {}, content_type='application/json')

    assert response.status_code == 404
    assert len(mail.outbox) == 0


@pytest.mark.parametrize('username,password', users)
def test_send_integration(db, client, mocker, username, password):
    mocked_send_issue = mocker.patch(
        'rdmo.projects.providers.SimpleIssueProvider.send_issue',
        return_value=HttpResponseRedirect('https://example.com/login/oauth/authorize')
    )
    client.login(username=username, password=password)
    issue = Issue.objects.get(pk=1)

    url = reverse(urlnames['send-integration'], args=[issue.project_id, issue.id])
    data = {
        'subject': 'Subject',
        'message': 'Message',
        'integration': 1
    }
    response = client.post(url, data, content_type='application/json')

    if issue.project_id in change_issue_permission_map.get(username, []):
        assert response.status_code == 200
        assert response.json() == {
            'redirect_url': 'https://example.com/login/oauth/authorize'
        }
        mocked_send_issue.assert_called_once()
    else:
        if issue.project_id in view_issue_permission_map.get(username, []):
            assert response.status_code == 403
        else:
            assert response.status_code == 404

        mocked_send_issue.assert_not_called()


@pytest.mark.parametrize('data', [
    {},
    {'integration': 2}
])
def test_send_integration_error(db, client, data):
    client.login(username='owner', password='owner')
    issue = Issue.objects.get(pk=1)

    url = reverse(urlnames['send-integration'], args=[issue.project_id, issue.id])
    request_data = {
        'subject': 'Subject',
        'message': 'Message',
        **data
    }
    response = client.post(url, request_data, content_type='application/json')

    assert response.status_code == 400
    assert 'integration' in response.json()


def test_send_integration_disabled(db, client, settings):
    settings.PROJECT_SEND_ISSUE = False
    client.login(username='owner', password='owner')
    issue = Issue.objects.get(pk=1)

    url = reverse(urlnames['send-integration'], args=[issue.project_id, issue.id])
    response = client.post(url, {}, content_type='application/json')

    assert response.status_code == 404
