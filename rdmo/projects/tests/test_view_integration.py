import pytest

from django.urls import reverse

from ..models import Integration, Issue

projects = [1, 2, 3, 4, 5]
integrations = [1, 2]


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
