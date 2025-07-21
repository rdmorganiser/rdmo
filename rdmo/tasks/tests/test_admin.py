from django.urls import reverse


def test_task_search(admin_client):
    url = reverse('admin:tasks_task_changelist') + '?q=test'
    response = admin_client.get(url)
    assert response.status_code == 200
