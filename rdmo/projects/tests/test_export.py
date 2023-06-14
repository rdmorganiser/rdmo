import os

from django.conf import settings
from django.urls import reverse


def test_project_answers_export_html(db, client):
    client.login(username='admin', password='admin')

    url = reverse('project_answers_export', args=[1, 'html'])
    response = client.get(url)

    assert response.status_code == 200

    test_file = os.path.join(settings.BASE_DIR, 'export', 'project.html')
    for a, b in zip(response.content.decode().splitlines(), open(test_file).read().splitlines()):
        assert a == b


def test_project_export_csv(db, client):
    client.login(username='admin', password='admin')

    url = reverse('project_export', args=[1, 'csvcomma'])
    response = client.get(url)

    assert response.status_code == 200

    test_file = os.path.join(settings.BASE_DIR, 'export', 'project.csv')
    for a, b in zip(response.content.decode().splitlines(), open(test_file).read().splitlines()):
        assert a == b
