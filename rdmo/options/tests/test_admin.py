from django.urls import reverse


def test_optionset_search(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:options_optionset_changelist') + '?q=test'
    response = client.get(url)
    assert response.status_code == 200


def test_option_search(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:options_option_changelist') + '?q=test'
    response = client.get(url)
    assert response.status_code == 200
