from django.conf import settings
from django.urls import reverse

from rdmo.projects.models import Project

urlnames = {
    'import': 'v1-projects:project-update-import',
}

project_id = 1

next_url = f'/projects/{project_id}/transfer/import/oauth/'

oauth_session_prefix = 'plugins.projects.imports.OAuthImport.oauth'

remote_project = {
    'title': 'Imported project',
    'description': 'This project was imported from the external service.'
}


def test_oauth_get_authorize(db, client, login, mocker):
    login('owner')

    mocked_request = mocker.patch('rdmo.services.client.requests.request')

    url = reverse(urlnames['import'], args=[project_id, 'oauth'])
    response = client.get(url)

    # without an access token, the frontend is told to redirect to the authorize url
    assert response.status_code == 200
    assert response.json()['redirect_url'].startswith(settings.OAUTH_PROVIDER['authorize_url'] + '?')
    assert client.session.get(f'{oauth_session_prefix}.oauth_next') == next_url

    mocked_request.assert_not_called()


def test_oauth_get(db, client, login, mocker):
    login('owner')
    session = client.session
    session[f'{oauth_session_prefix}.oauth_access_token'] = 'access_token'
    session.save()

    mocked_request = mocker.patch('rdmo.services.client.requests.request')
    mocked_request.return_value.status_code = 200
    mocked_request.return_value.json.return_value = {'project': remote_project}

    url = reverse(urlnames['import'], args=[project_id, 'oauth'])
    response = client.get(url)

    assert response.status_code == 200
    assert 'html' in response.json()

    assert mocked_request.call_args.args == ('get', settings.OAUTH_PROVIDER_URL)


def test_oauth_post(db, client, login):
    login('owner')
    session = client.session
    session[f'{oauth_session_prefix}.oauth_access_token'] = 'access_token'
    session[f'{oauth_session_prefix}.project'] = remote_project
    session.save()

    url = reverse(urlnames['import'], args=[project_id, 'oauth'])
    response = client.post(url)

    assert response.status_code == 200
    assert response.json() == {'location': {'area': 'transfer'}}

    project = Project.objects.get(id=project_id)
    assert project.title == remote_project['title']
    assert project.description == remote_project['description']


def test_oauth_post_cancel(db, client, login, mocker):
    login('owner')
    session = client.session
    session[f'{oauth_session_prefix}.oauth_access_token'] = 'access_token'
    session[f'{oauth_session_prefix}.project'] = remote_project
    session.save()

    project = Project.objects.get(id=project_id)
    title = project.title

    mocked_request = mocker.patch('rdmo.services.client.requests.request')

    url = reverse(urlnames['import'], args=[project_id, 'oauth'])
    response = client.post(url, {'cancel': ''})

    assert response.status_code == 200
    assert response.json() == {'location': {'area': 'transfer'}}

    project.refresh_from_db()
    assert project.title == title

    mocked_request.assert_not_called()
