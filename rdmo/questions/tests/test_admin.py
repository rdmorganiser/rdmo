from django.urls import reverse


def test_catalog_search(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:questions_catalog_changelist') + '?q=test'
    response = client.get(url)
    assert response.status_code == 200


def test_section_search(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:questions_section_changelist') + '?q=test'
    response = client.get(url)
    assert response.status_code == 200


def test_page_search(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:questions_page_changelist') + '?q=test'
    response = client.get(url)
    assert response.status_code == 200


def test_questionset_search(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:questions_questionset_changelist') + '?q=test'
    response = client.get(url)
    assert response.status_code == 200


def test_question_search(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:questions_question_changelist') + '?q=test'
    response = client.get(url)
    assert response.status_code == 200
