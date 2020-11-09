from django.urls import reverse


def test_condition_search(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:conditions_condition_changelist') + '?q=test'
    response = client.get(url)
    assert response.status_code == 200
