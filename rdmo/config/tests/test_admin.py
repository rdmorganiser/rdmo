from django.urls import reverse


def test_plugin_search(admin_client):
    url = reverse('admin:config_plugin_changelist') + '?q=test'
    response = admin_client.get(url)
    assert response.status_code == 200
