from django.urls import reverse


def test_catalog_search(admin_client):
    url = reverse('admin:questions_catalog_changelist') + '?q=test'
    response = admin_client.get(url)
    assert response.status_code == 200


def test_section_search(admin_client):
    url = reverse('admin:questions_section_changelist') + '?q=test'
    response = admin_client.get(url)
    assert response.status_code == 200


def test_page_search(admin_client):
    url = reverse('admin:questions_page_changelist') + '?q=test'
    response = admin_client.get(url)
    assert response.status_code == 200


def test_questionset_search(admin_client):
    url = reverse('admin:questions_questionset_changelist') + '?q=test'
    response = admin_client.get(url)
    assert response.status_code == 200


def test_question_search(admin_client):
    url = reverse('admin:questions_question_changelist') + '?q=test'
    response = admin_client.get(url)
    assert response.status_code == 200
