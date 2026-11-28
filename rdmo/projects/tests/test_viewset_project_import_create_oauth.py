from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse

from rdmo.projects.models import Project
from rdmo.questions.models import Catalog

urlnames = {
    'import': 'v1-projects:project-create-import',
}

next_url = '/projects/import/oauth/'

oauth_session_prefix = 'plugins.projects.imports.OAuthImport.oauth'

remote_project = {
    'title': 'Imported project',
    'description': 'This project was imported from the external service.'
}


def test_oauth_get_authorize(db, client, login, mocker):
    login('user')

    mocked_request = mocker.patch('rdmo.services.client.requests.request')

    url = reverse(urlnames['import'], args=['oauth'])
    response = client.get(url)

    # without an access token, the frontend is told to redirect to the authorize url
    assert response.status_code == 200
    assert response.json()['redirect_url'].startswith(settings.OAUTH_PROVIDER['authorize_url'] + '?')
    assert client.session.get(f'{oauth_session_prefix}.oauth_next') == next_url

    mocked_request.assert_not_called()


def test_oauth_get(db, client, login, mocker):
    login('user')
    session = client.session
    session[f'{oauth_session_prefix}.oauth_access_token'] = 'access_token'
    session.save()

    mocked_request = mocker.patch('rdmo.services.client.requests.request')
    mocked_request.return_value.status_code = 200
    mocked_request.return_value.json.return_value = {'project': remote_project}

    url = reverse(urlnames['import'], args=['oauth'])
    response = client.get(url)

    assert response.status_code == 200
    assert 'html' in response.json()

    assert mocked_request.call_args.args == ('get', settings.OAUTH_PROVIDER_URL)


def test_oauth_post(db, client, login):
    login('user')
    user = User.objects.get(username='user')

    # use the last available catalog, to see that the catalog from the service is used
    catalog = Catalog.objects.filter_for_user(user).last()

    session = client.session
    session[f'{oauth_session_prefix}.oauth_access_token'] = 'access_token'
    session[f'{oauth_session_prefix}.project'] = {**remote_project, 'catalog': catalog.uri}
    session.save()

    project_count = Project.objects.count()

    url = reverse(urlnames['import'], args=['oauth'])
    response = client.post(url)

    # a new project is created and the user is redirected to it
    assert response.status_code == 200
    assert Project.objects.count() == project_count + 1

    project = Project.objects.order_by('-id').first()
    assert response.json() == {'redirect_url': reverse('project', args=[project.id])}

    assert project.title == remote_project['title']
    assert project.description == remote_project['description']
    assert project.catalog == catalog
    assert project.site_id == settings.SITE_ID
    assert project.memberships.filter(user=user, role='owner').exists()


def test_oauth_post_cancel(db, client, login, mocker):
    login('user')
    session = client.session
    session[f'{oauth_session_prefix}.oauth_access_token'] = 'access_token'
    session[f'{oauth_session_prefix}.project'] = remote_project
    session.save()

    project_count = Project.objects.count()

    mocked_request = mocker.patch('rdmo.services.client.requests.request')

    url = reverse(urlnames['import'], args=['oauth'])
    response = client.post(url, {'cancel': ''})

    # no project is created
    assert response.status_code == 200
    assert response.json() == {'success': True}
    assert Project.objects.count() == project_count

    mocked_request.assert_not_called()
