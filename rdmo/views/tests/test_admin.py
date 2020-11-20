from django.urls import reverse


def test_view_search(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:views_view_changelist') + '?q=test'
    response = client.get(url)
    assert response.status_code == 200
