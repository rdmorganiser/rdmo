from django.urls import reverse


def test_condition_search(admin_client):
    url = reverse('admin:conditions_condition_changelist') + '?q=test'
    response = admin_client.get(url)
    assert response.status_code == 200
