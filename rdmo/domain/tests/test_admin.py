from django.urls import reverse


def test_attribute_search(admin_client):
    url = reverse('admin:domain_attribute_changelist') + '?q=test'
    response = admin_client.get(url)
    assert response.status_code == 200
