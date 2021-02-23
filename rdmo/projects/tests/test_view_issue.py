import pytest
from django.core import mail
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
    'owner': [1, 2, 3, 4, 5],
    'manager': [1, 3, 5],
    'author': [1, 3, 5],
    'guest': [1, 3, 5],
    'api': [1, 2, 3, 4, 5],
    'site': [1, 2, 3, 4, 5]
}

change_issue_permission_map = {
    'owner': [1, 2, 3, 4, 5],
    'manager': [1, 3, 5],
    'author': [1, 3, 5],
    'api': [1, 2, 3, 4, 5],
    'site': [1, 2, 3, 4, 5]
}

delete_issue_permission_map = {
    'owner': [1, 2, 3, 4, 5],
    'manager': [1, 3, 5],
    'api': [1, 2, 3, 4, 5],
    'site': [1, 2, 3, 4, 5]
}


projects = [1, 2, 3, 4, 5]
issues = [1, 2, 3, 4]

integration_pk = 1

issue_status = ('open', 'in_progress', 'closed')


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('issue_id', issues)
def test_issue_update_get(db, client, username, password, project_id, issue_id):
    client.login(username=username, password=password)
    issue = Issue.objects.filter(project_id=project_id, id=issue_id).first()

    url = reverse('issue_update', args=[project_id, issue_id])
    response = client.get(url)

    if issue:
        if project_id in change_issue_permission_map.get(username, []):
            assert response.status_code == 200
        elif password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('issue_id', issues)
@pytest.mark.parametrize('status', issue_status)
def test_issue_update_post(db, client, username, password, project_id, issue_id, status):
    client.login(username=username, password=password)
    issue = Issue.objects.filter(project_id=project_id, id=issue_id).first()

    url = reverse('issue_update', args=[project_id, issue_id])
    data = {
        'status': status
    }
    response = client.post(url, data)

    if issue:
        if project_id in change_issue_permission_map.get(username, []):
            assert response.status_code == 302
            assert Issue.objects.get(id=issue_id).status == status
        else:
            if password:
                assert response.status_code == 403
            else:
                assert response.status_code == 302

            assert Issue.objects.get(id=issue_id).status == issue.status
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('issue_id', issues)
@pytest.mark.parametrize('project_id', projects)
def test_issue_send_get(db, client, username, password, project_id, issue_id):
    client.login(username=username, password=password)
    issue = Issue.objects.filter(project_id=project_id, id=issue_id).first()

    url = reverse('issue_update', args=[project_id, issue_id])
    response = client.get(url)

    if issue:
        if project_id in change_issue_permission_map.get(username, []):
            assert response.status_code == 200
        elif password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('issue_id', issues)
@pytest.mark.parametrize('project_id', projects)
def test_issue_send_post_email(db, client, username, password, project_id, issue_id):
    client.login(username=username, password=password)
    issue = Issue.objects.filter(project_id=project_id, id=issue_id).first()

    url = reverse('issue_send', args=[project_id, issue_id])
    data = {
        'subject': 'Subject',
        'message': 'Message',
        'recipients': ['email@example.com']
    }
    response = client.post(url, data)

    if issue:
        if project_id in change_issue_permission_map.get(username, []):
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
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('issue_id', issues)
@pytest.mark.parametrize('project_id', projects)
def test_issue_send_post_attachements(db, client, files, username, password, project_id, issue_id):
    client.login(username=username, password=password)
    issue = Issue.objects.filter(project_id=project_id, id=issue_id).first()

    if issue:
        view = issue.project.views.first()
        file = issue.project.values.filter(snapshot=None, value_type=VALUE_TYPE_FILE).first()

        if file and view:
            url = reverse('issue_send', args=[project_id, issue_id])
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

            if project_id in change_issue_permission_map.get(username, []):
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
@pytest.mark.parametrize('project_id', projects)
def test_issue_send_post_integration(db, client, username, password, project_id, issue_id):
    client.login(username=username, password=password)
    issue = Issue.objects.filter(project_id=project_id, id=issue_id).first()

    url = reverse('issue_send', args=[project_id, issue_id])
    data = {
        'subject': 'Subject',
        'message': 'Message',
        'integration': [integration_pk]
    }
    response = client.post(url, data)

    if issue:
        if project_id in change_issue_permission_map.get(username, []):
            if integration_pk in Project.objects.get(pk=project_id).integrations.values_list('id', flat=True):
                assert response.status_code == 302
                assert response.url.startswith('https://github.com')
            else:
                assert response.status_code == 200
        else:
            if password:
                assert response.status_code == 403
            else:
                assert response.status_code == 302
                assert not response.url.startswith('https://github.com')
    else:
        assert response.status_code == 404
