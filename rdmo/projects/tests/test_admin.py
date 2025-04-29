from django.urls import reverse


def test_project_search(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:projects_project_changelist') + '?q=test'
    response = client.get(url)

    assert response.status_code == 200


def test_membership_search(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:projects_membership_changelist') + '?q=test'
    response = client.get(url)

    assert response.status_code == 200


def test_continuation_search(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:projects_continuation_changelist') + '?q=test'
    response = client.get(url)

    assert response.status_code == 200


def test_visibility_search(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:projects_visibility_changelist') + '?q=test'
    response = client.get(url)

    assert response.status_code == 200


def test_integration_search(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:projects_integration_changelist') + '?q=test'
    response = client.get(url)

    assert response.status_code == 200


def test_integrationoption_search(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:projects_integrationoption_changelist') + '?q=test'
    response = client.get(url)

    assert response.status_code == 200


def test_invite_search(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:projects_invite_changelist') + '?q=test'
    response = client.get(url)

    assert response.status_code == 200


def test_issue_search(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:projects_issue_changelist') + '?q=test'
    response = client.get(url)

    assert response.status_code == 200


def test_issueresource_search(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:projects_issueresource_changelist') + '?q=test'
    response = client.get(url)

    assert response.status_code == 200


def test_snapshot_search(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:projects_snapshot_changelist') + '?q=test'
    response = client.get(url)

    assert response.status_code == 200


def test_value_search(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:projects_value_changelist') + '?q=test'
    response = client.get(url)

    assert response.status_code == 200
