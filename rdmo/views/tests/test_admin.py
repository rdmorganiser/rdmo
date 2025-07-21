from django.urls import reverse


def test_view_search(admin_client):
    url = reverse('admin:views_view_changelist') + '?q=test'
    response = admin_client.get(url)
    assert response.status_code == 200
