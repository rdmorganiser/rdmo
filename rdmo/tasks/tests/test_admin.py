from django.urls import reverse


def test_task_search(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:tasks_task_changelist') + '?q=test'
    response = client.get(url)
    assert response.status_code == 200
