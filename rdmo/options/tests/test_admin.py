from django.urls import reverse


def test_optionset_search(admin_client):
    url = reverse('admin:options_optionset_changelist') + '?q=test'
    response = admin_client.get(url)
    assert response.status_code == 200


def test_option_search(admin_client):
    url = reverse('admin:options_option_changelist') + '?q=test'
    response = admin_client.get(url)
    assert response.status_code == 200
