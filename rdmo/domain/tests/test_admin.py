from django.urls import reverse


def test_attribute_search(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:domain_attribute_changelist') + '?q=test'
    response = client.get(url)
    assert response.status_code == 200
