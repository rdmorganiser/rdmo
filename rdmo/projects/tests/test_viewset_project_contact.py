import pytest

from django.core import mail
from django.urls import reverse

from rdmo.projects.models import Project, Value
from rdmo.questions.models import Page, Question

users = (
    ('owner', 'owner'),
    ('manager', 'manager'),
    ('author', 'author'),
    ('guest', 'guest'),
    ('api', 'api'),
    ('user', 'user'),
    ('site', 'site'),
    ('anonymous', None),
)

view_project_permission_map = {
    'owner': [1, 2, 3, 4, 5, 10, 12],
    'manager': [1, 3, 5, 7, 12],
    'author': [1, 3, 5, 8, 12],
    'guest': [1, 3, 5, 9, 12],
    'user': [12],
    'api': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'site': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
}

change_project_permission_map = {
    'owner': [1, 2, 3, 4, 5, 10, 12],
    'manager': [1, 3, 5, 7],
    'api': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12],
    'site': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12]
}

delete_project_permission_map = {
    'owner': [1, 2, 3, 4, 5, 10, 12],
    'api': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12],
    'site': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12]
}

urlnames = {
    'contact': 'v1-projects:project-contact'
}

projects = [1, 2, 3, 4, 5, 12]
projects_internal = [12]
conditions = [1]

@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_contact_get(db, client, username, password, project_id):
    client.login(username=username, password=password)

    project = Project.objects.get(pk=project_id)

    url = reverse(urlnames['contact'], args=[project_id])
    response = client.get(url)

    if project_id in view_project_permission_map.get(username, []):
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json().get('subject')
        assert response.json().get('message')
        assert f'regarding the project "{project.title}":' in response.json().get('message')
    else:
        if password:
            assert response.status_code == 404
        else:
            assert response.status_code == 401

def test_contact_get_page(db, client):
    client.login(username='guest', password='guest')

    project = Project.objects.get(pk=1)
    page = Page.objects.get(pk=1)

    url = reverse(urlnames['contact'], args=[project.id]) + f'?page={page.id}'
    response = client.get(url)

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json().get('subject')
    assert f'regarding the project "{project.title}" on the page "{page.title}":' in response.json().get('message')


def test_contact_get_question(db, client):
    client.login(username='guest', password='guest')

    project = Project.objects.get(pk=1)
    question = Question.objects.get(pk=1)

    url = reverse(urlnames['contact'], args=[project.id]) + f'?question={question.id}'
    response = client.get(url)

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json().get('subject')
    assert f'In particular, about the question: {question.text}' in response.json().get('message')


def test_contact_get_value(db, client):
    client.login(username='guest', password='guest')

    project = Project.objects.get(pk=1)
    value = Value.objects.get(pk=1)

    url = reverse(urlnames['contact'], args=[project.id]) + f'?values={value.id}'
    response = client.get(url)

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json().get('subject')
    assert f'Answer: {value.value}' in response.json().get('message')


def test_contact_get_values(db, client):
    client.login(username='guest', password='guest')

    project = Project.objects.get(pk=1)
    value1 = Value.objects.get(pk=8)
    value2 = Value.objects.get(pk=9)

    url = reverse(urlnames['contact'], args=[project.id]) + f'?values={value1.id}&values={value2.id}'
    response = client.get(url)

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json().get('subject')
    assert f'* {value1.value}' in response.json().get('message')
    assert f'* {value2.value}' in response.json().get('message')


def test_contact_get_set(db, client):
    client.login(username='guest', password='guest')

    project = Project.objects.get(pk=1)
    page = Page.objects.get(pk=42)
    value = Value.objects.get(pk=47)
    set_value = Value.objects.get(id=85)

    url = reverse(urlnames['contact'], args=[project.id]) + f'?page={page.id}&values={value.id}'
    response = client.get(url)

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json().get('subject')
    assert f'Set: {set_value.value}' in response.json().get('message')


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_contact_post(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['contact'], args=[project_id])
    response = client.post(url, {
        'subject': 'Test subject',
        'message': 'Test message'
    })

    if project_id in view_project_permission_map.get(username, []):
        assert response.status_code == 204
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == '[example.com] Test subject'
        assert mail.outbox[0].body == 'Test message'
    else:
        if password:
            assert response.status_code == 404
        else:
            assert response.status_code == 401

        assert len(mail.outbox) == 0


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_contact_post_error(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['contact'], args=[project_id])
    response = client.post(url, {})

    if project_id in view_project_permission_map.get(username, []):
        assert response.status_code == 400
        assert len(mail.outbox) == 0
    else:
        if password:
            assert response.status_code == 404
        else:
            assert response.status_code == 401

        assert len(mail.outbox) == 0
