import pytest

from django.urls import reverse

from ..models import Integration, Issue

users = (
    ('owner', 'owner'),
    ('manager', 'manager'),
    ('author', 'author'),
    ('guest', 'guest'),
    ('user', 'user'),
    ('site', 'site'),
    ('anonymous', None),
)

view_integration_permission_map = {
    'owner': [1, 2, 3, 4, 5],
    'manager': [1, 3, 5],
    'author': [1, 3, 5],
    'guest': [1, 3, 5],
    'api': [1, 2, 3, 4, 5],
    'site': [1, 2, 3, 4, 5]
}

add_integration_permission_map = change_integration_permission_map = delete_integration_permission_map = {
    'owner': [1, 2, 3, 4, 5],
    'manager': [1, 3, 5],
    'api': [1, 2, 3, 4, 5],
    'site': [1, 2, 3, 4, 5]
}

projects = [1, 2, 3, 4, 5]
integrations = [1, 2]


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_integration_create_get(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('integration_create', args=[project_id, 'simple'])
    response = client.get(url)

    if project_id in add_integration_permission_map.get(username, []):
        assert response.status_code == 200
    elif password:
        assert response.status_code == 403
    else:
        assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_integration_create_post(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('integration_create', args=[project_id, 'simple'])
    data = {
        'project_url': 'https://example.com/projects/1'
    }
    response = client.post(url, data)

    if project_id in add_integration_permission_map.get(username, []):
        assert response.status_code == 302
        values = Integration.objects.order_by('id').last().options.values('key', 'value', 'secret')
        assert sorted(values, key=lambda obj: obj['key']) == [
            {
                'key': 'project_url',
                'value': 'https://example.com/projects/1',
                'secret': False
            },
            {
                'key': 'secret',
                'value': '',
                'secret': True
            }
        ]
    elif password:
        assert response.status_code == 403
    else:
        assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('integration_id', integrations)
def test_integration_update_get(db, client, username, password, project_id, integration_id):
    client.login(username=username, password=password)
    integration = Integration.objects.filter(project_id=project_id, id=integration_id).first()

    url = reverse('integration_update', args=[project_id, integration_id])
    response = client.get(url)

    if integration:
        if project_id in change_integration_permission_map.get(username, []):
            assert response.status_code == 200
        elif password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('integration_id', integrations)
def test_integration_update_post(db, client, username, password, project_id, integration_id):
    client.login(username=username, password=password)
    integration = Integration.objects.filter(project_id=project_id, id=integration_id).first()

    url = reverse('integration_update', args=[project_id, integration_id])
    data = {
        'project_url': 'https://example.com/projects/2',
        'secret': 'super_secret'
    }
    response = client.post(url, data)

    if integration:
        if project_id in change_integration_permission_map.get(username, []):
            assert response.status_code == 302
            values = Integration.objects.filter(project_id=project_id, id=integration_id).first() \
                                        .options.values('key', 'value', 'secret')
            assert sorted(values, key=lambda obj: obj['key']) == [
                {
                    'key': 'project_url',
                    'value': 'https://example.com/projects/2',
                    'secret': False
                },
                {
                    'key': 'secret',
                    'value': 'super_secret',
                    'secret': True
                }
            ]
        elif password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('integration_id', integrations)
def test_integration_delete_get(db, client, username, password, project_id, integration_id):
    client.login(username=username, password=password)
    integration = Integration.objects.filter(project_id=project_id, id=integration_id).first()

    url = reverse('integration_delete', args=[project_id, integration_id])
    response = client.get(url)

    if integration:
        if project_id in delete_integration_permission_map.get(username, []):
            assert response.status_code == 200
        elif password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('integration_id', integrations)
def test_integration_delete_post(db, client, username, password, project_id, integration_id):
    client.login(username=username, password=password)
    integration = Integration.objects.filter(project_id=project_id, id=integration_id).first()

    url = reverse('integration_delete', args=[project_id, integration_id])
    response = client.delete(url)

    if integration:
        if project_id in delete_integration_permission_map.get(username, []):
            assert response.status_code == 302
            assert Integration.objects.filter(project_id=project_id, id=integration_id).first() is None
        elif password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('integration_id', integrations)
def test_integration_webhook_get(db, client, project_id, integration_id):
    url = reverse('integration_webhook', args=[project_id, integration_id])
    response = client.get(url)

    assert response.status_code == 405
    assert Issue.objects.filter(status='closed').count() == 0


@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('integration_id', integrations)
def test_integration_webhook_post(db, client, project_id, integration_id):
    integration = Integration.objects.filter(project_id=project_id, id=integration_id).first()

    secret = 'super_duper_secret'
    url = reverse('integration_webhook', args=[project_id, integration_id])
    data = {
        'action': 'closed',
        'url': 'https://simple.example.com/issues/1'
    }

    response = client.post(url, data, **{'HTTP_X_SECRET': secret, 'content_type': 'application/json'})

    if integration:
        assert response.status_code == 200
        assert Issue.objects.filter(status='closed').count() == (1 if integration_id == 1 else 0)
    else:
        assert response.status_code == 404
        assert Issue.objects.filter(status='closed').count() == 0


@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('integration_id', integrations)
def test_integration_webhook_post_wrong_url(db, client, project_id, integration_id):
    integration = Integration.objects.filter(project_id=project_id, id=integration_id).first()

    secret = 'super_duper_secret'
    url = reverse('integration_webhook', args=[project_id, integration_id])
    data = {
        'action': 'closed',
        'url': 'https://simple.example.com/issues/2'
    }

    response = client.post(url, data, **{'HTTP_X_SECRET': secret, 'content_type': 'application/json'})

    if integration:
        assert response.status_code == 200
        assert Issue.objects.filter(status='closed').count() == 0
    else:
        assert response.status_code == 404
        assert Issue.objects.filter(status='closed').count() == 0


@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('integration_id', integrations)
def test_integration_webhook_post_no_secret(db, client, project_id, integration_id):
    url = reverse('integration_webhook', args=[project_id, integration_id])
    response = client.post(url, {})

    assert response.status_code == 404
    assert Issue.objects.filter(status='closed').count() == 0
