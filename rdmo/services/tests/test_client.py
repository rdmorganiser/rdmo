import io
from urllib.parse import parse_qs, urlparse

import pytest

from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.backends.db import SessionStore
from django.http import HttpResponse
from django.urls import reverse

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

from rdmo.core.plugins import Plugin
from rdmo.services.client import OauthClient
from rdmo.services.exceptions import OauthAuthorizationRequired

authorize_url = 'https://example.com/oauth/authorize'
token_url = 'https://example.com/oauth/token'
api_url = 'https://example.com/api/'


def get_redirect_uri():
    return 'http://testserver' + reverse('oauth_callback', args=['example'])


def get_request(rf, session, params=None):
    request = rf.get('/', params or {})
    request.session = session
    request.user = AnonymousUser()
    return request


@pytest.fixture
def plugin(db, rf):
    plugin = Plugin('example', 'Example', 'example.Plugin')
    plugin.request = get_request(rf, SessionStore())
    return plugin


@pytest.fixture
def oauth_client(plugin):
    return OauthClient(
        plugin,
        authorize_url=authorize_url,
        token_url=token_url,
        client_id='client_id',
        client_secret='client_secret',
        scope='write'
    )


@pytest.fixture
def scoped_session(plugin):
    class TestScopedSession:
        def get(self, key):
            return plugin.request.session.get(f'example.Plugin.example.{key}')

        def set(self, key, value):
            plugin.request.session[f'example.Plugin.example.{key}'] = value

    return TestScopedSession()


def mock_token_response(mocker, status_code=200, json=None):
    response = mocker.Mock(status_code=status_code, content=b'')
    response.json.return_value = json or {}
    if status_code >= 400:
        response.raise_for_status.side_effect = requests.HTTPError
    return response


@pytest.mark.parametrize('method', ['get', 'post', 'put', 'delete'])
def test_send(plugin, oauth_client, scoped_session, mocker, method):
    scoped_session.set('oauth_access_token', 'access_token')

    mocked_request = mocker.patch('rdmo.services.client.requests.request')
    mocked_request.return_value.status_code = 200

    response = getattr(oauth_client, method)(api_url, json={'foo': 'bar'}, headers={'Accept': 'application/json'})

    assert response == mocked_request.return_value

    args, kwargs = mocked_request.call_args
    assert args == (method, api_url)
    assert kwargs['json'] == {'foo': 'bar'}
    assert kwargs['headers'] == {'Authorization': 'Bearer access_token', 'Accept': 'application/json'}
    assert kwargs['timeout'] == 30


def test_send_without_token(plugin, oauth_client, mocker):
    mocked_request = mocker.patch('rdmo.services.client.requests.request')

    with pytest.raises(OauthAuthorizationRequired):
        oauth_client.get(api_url)

    mocked_request.assert_not_called()


def test_send_expired(plugin, oauth_client, scoped_session, mocker):
    scoped_session.set('oauth_access_token', 'expired_token')
    scoped_session.set('oauth_refresh_token', 'refresh_token')
    scoped_session.set('oauth_expires_at', 0)

    mocked_post = mocker.patch('rdmo.services.client.requests.post')
    mocked_post.return_value = mock_token_response(mocker, json={
        'access_token': 'new_access_token',
        'refresh_token': 'new_refresh_token',
        'expires_in': 3600
    })

    mocked_request = mocker.patch('rdmo.services.client.requests.request')
    mocked_request.return_value.status_code = 200

    oauth_client.get(api_url)

    # the expired access token is renewed before the request
    args, kwargs = mocked_post.call_args
    assert args == (token_url, )
    assert kwargs['data'] == {
        'grant_type': 'refresh_token',
        'refresh_token': 'refresh_token',
        'client_id': 'client_id',
        'client_secret': 'client_secret'
    }

    assert mocked_request.call_args.kwargs['headers']['Authorization'] == 'Bearer new_access_token'

    assert scoped_session.get('oauth_access_token') == 'new_access_token'
    assert scoped_session.get('oauth_refresh_token') == 'new_refresh_token'
    assert scoped_session.get('oauth_expires_at') > 0


def test_send_unauthorized(plugin, oauth_client, scoped_session, mocker):
    scoped_session.set('oauth_access_token', 'access_token')

    mocked_request = mocker.patch('rdmo.services.client.requests.request')
    mocked_request.return_value = mocker.Mock(status_code=401, content=b'')

    # without a refresh token, the invalid access token is removed
    with pytest.raises(OauthAuthorizationRequired):
        oauth_client.get(api_url)

    assert mocked_request.call_count == 1
    assert scoped_session.get('oauth_access_token') is None


def test_send_unauthorized_refresh(plugin, oauth_client, scoped_session, mocker):
    scoped_session.set('oauth_access_token', 'access_token')
    scoped_session.set('oauth_refresh_token', 'refresh_token')

    mocked_post = mocker.patch('rdmo.services.client.requests.post')
    mocked_post.return_value = mock_token_response(mocker, json={'access_token': 'new_access_token'})

    mocked_request = mocker.patch('rdmo.services.client.requests.request')
    mocked_request.side_effect = [
        mocker.Mock(status_code=401, content=b''),
        mocker.Mock(status_code=200)
    ]

    response = oauth_client.get(api_url)

    # the access token is refreshed after the 401 and the request is repeated
    assert response.status_code == 200
    assert mocked_request.call_count == 2
    assert mocked_request.call_args_list[1].kwargs['headers']['Authorization'] == 'Bearer new_access_token'

    # the old refresh token is kept, since none was returned
    assert scoped_session.get('oauth_access_token') == 'new_access_token'
    assert scoped_session.get('oauth_refresh_token') == 'refresh_token'


def test_send_unauthorized_after_refresh(plugin, oauth_client, scoped_session, mocker):
    scoped_session.set('oauth_access_token', 'access_token')
    scoped_session.set('oauth_refresh_token', 'refresh_token')

    mocked_post = mocker.patch('rdmo.services.client.requests.post')
    mocked_post.return_value = mock_token_response(mocker, json={'access_token': 'new_access_token'})

    mocked_request = mocker.patch('rdmo.services.client.requests.request')
    mocked_request.return_value = mocker.Mock(status_code=401, content=b'')

    # the request is repeated only once, then the tokens are removed
    with pytest.raises(OauthAuthorizationRequired):
        oauth_client.get(api_url)

    assert mocked_request.call_count == 2
    assert scoped_session.get('oauth_access_token') is None
    assert scoped_session.get('oauth_refresh_token') is None


def test_send_refresh_error(plugin, oauth_client, scoped_session, mocker):
    scoped_session.set('oauth_access_token', 'expired_token')
    scoped_session.set('oauth_refresh_token', 'refresh_token')
    scoped_session.set('oauth_expires_at', 0)

    mocked_post = mocker.patch('rdmo.services.client.requests.post')
    mocked_post.return_value = mock_token_response(mocker, status_code=400)

    mocked_request = mocker.patch('rdmo.services.client.requests.request')

    # if the refresh fails, the tokens are removed
    with pytest.raises(OauthAuthorizationRequired):
        oauth_client.get(api_url)

    mocked_request.assert_not_called()
    assert scoped_session.get('oauth_access_token') is None
    assert scoped_session.get('oauth_refresh_token') is None
    assert scoped_session.get('oauth_expires_at') is None



def test_upload(plugin, oauth_client, scoped_session, mocker):
    scoped_session.set('oauth_access_token', 'access_token')

    mocked_request = mocker.patch('rdmo.services.client.requests.request')
    mocked_request.return_value.status_code = 200

    oauth_client.upload(api_url, {'file': ('example.txt', b'file content', 'text/plain')}, data={'title': 'Title'})

    args, kwargs = mocked_request.call_args
    assert args == ('post', api_url)
    assert kwargs['headers']['Authorization'] == 'Bearer access_token'
    assert kwargs['headers']['Content-Type'].startswith('multipart/form-data; boundary=')

    # the files and the additional fields are sent in the multipart body
    assert isinstance(kwargs['data'], MultipartEncoder)
    body = kwargs['data'].to_string()
    assert b'name="title"' in body
    assert b'filename="example.txt"' in body
    assert b'file content' in body


def test_upload_unauthorized_refresh(plugin, oauth_client, scoped_session, mocker):
    scoped_session.set('oauth_access_token', 'access_token')
    scoped_session.set('oauth_refresh_token', 'refresh_token')

    mocked_post = mocker.patch('rdmo.services.client.requests.post')
    mocked_post.return_value = mock_token_response(mocker, json={'access_token': 'new_access_token'})

    # the fake request reads the body, like requests would do
    bodies = []
    responses = [mocker.Mock(status_code=401, content=b''), mocker.Mock(status_code=200)]

    def fake_request(method, url, **kwargs):
        bodies.append(kwargs['data'].to_string())
        return responses.pop(0)

    mocker.patch('rdmo.services.client.requests.request', side_effect=fake_request)

    response = oauth_client.upload(api_url, {'file': ('example.txt', io.BytesIO(b'file content'), 'text/plain')})

    # the repeated request has the complete body again, since the file was rewound
    assert response.status_code == 200
    assert len(bodies) == 2
    assert b'file content' in bodies[0]
    assert b'file content' in bodies[1]

def test_authorize(plugin, oauth_client, scoped_session):
    url = oauth_client.authorize('/next/')

    assert url.startswith(authorize_url + '?')
    assert parse_qs(urlparse(url).query) == {
        'response_type': ['code'],
        'client_id': ['client_id'],
        'redirect_uri': [get_redirect_uri()],
        'state': [scoped_session.get('oauth_state')],
        'scope': ['write']
    }

    assert scoped_session.get('oauth_next') == '/next/'
    assert oauth_client.is_pending()


def test_redirect(plugin, oauth_client, scoped_session):
    response = oauth_client.redirect('/next/')

    assert response.data['redirect_url'].startswith(authorize_url + '?')
    assert scoped_session.get('oauth_next') == '/next/'


def test_callback(rf, plugin, oauth_client, scoped_session, mocker):
    scoped_session.set('oauth_state', 'state')
    scoped_session.set('oauth_next', '/next/')
    plugin.request = get_request(rf, plugin.request.session, {'state': 'state', 'code': 'code'})

    mocked_post = mocker.patch('rdmo.services.client.requests.post')
    mocked_post.return_value = mock_token_response(mocker, json={
        'access_token': 'access_token',
        'refresh_token': 'refresh_token',
        'expires_in': 3600
    })

    response = oauth_client.callback()

    assert response.status_code == 302
    assert response.url == '/next/'

    args, kwargs = mocked_post.call_args
    assert args == (token_url, )
    assert kwargs['data'] == {
        'grant_type': 'authorization_code',
        'code': 'code',
        'redirect_uri': get_redirect_uri(),
        'client_id': 'client_id',
        'client_secret': 'client_secret'
    }

    assert scoped_session.get('oauth_access_token') == 'access_token'
    assert scoped_session.get('oauth_refresh_token') == 'refresh_token'
    assert scoped_session.get('oauth_expires_at') > 0
    assert scoped_session.get('oauth_state') is None
    assert scoped_session.get('oauth_next') is None
    assert not oauth_client.is_pending()


def test_callback_state_mismatch(rf, plugin, oauth_client, scoped_session, mocker):
    scoped_session.set('oauth_state', 'state')
    scoped_session.set('oauth_next', '/next/')
    plugin.request = get_request(rf, plugin.request.session, {'state': 'wrong', 'code': 'code'})

    mocked_post = mocker.patch('rdmo.services.client.requests.post')
    mocked_render_error = mocker.patch.object(OauthClient, 'render_error', return_value=HttpResponse())

    oauth_client.callback()

    assert str(mocked_render_error.call_args.args[1]) == 'State parameter did not match.'
    mocked_post.assert_not_called()
    assert scoped_session.get('oauth_access_token') is None


def test_callback_error(rf, plugin, oauth_client, scoped_session, mocker):
    scoped_session.set('oauth_state', 'state')
    scoped_session.set('oauth_next', '/next/')
    plugin.request = get_request(rf, plugin.request.session, {'state': 'state', 'error': 'access_denied'})

    mocked_post = mocker.patch('rdmo.services.client.requests.post')
    mocked_render_error = mocker.patch.object(OauthClient, 'render_error', return_value=HttpResponse())

    oauth_client.callback()

    # the error of the authorization server is shown and no token is requested
    assert mocked_render_error.call_args.args[1] == 'access_denied'
    mocked_post.assert_not_called()
    assert scoped_session.get('oauth_access_token') is None


def test_callback_token_error(rf, plugin, oauth_client, scoped_session, mocker):
    scoped_session.set('oauth_state', 'state')
    scoped_session.set('oauth_next', '/next/')
    plugin.request = get_request(rf, plugin.request.session, {'state': 'state', 'code': 'code'})

    mocked_post = mocker.patch('rdmo.services.client.requests.post')
    mocked_post.return_value = mock_token_response(mocker, status_code=400, json={'error': 'invalid_grant'})
    mocked_render_error = mocker.patch.object(OauthClient, 'render_error', return_value=HttpResponse())

    oauth_client.callback()

    # the error of the token endpoint is shown and no token is stored
    assert mocked_render_error.call_args.args[1] == 'invalid_grant'
    assert scoped_session.get('oauth_access_token') is None


def test_callback_external_next_url(rf, plugin, oauth_client, scoped_session, mocker):
    scoped_session.set('oauth_state', 'state')
    scoped_session.set('oauth_next', 'https://example.org/')
    plugin.request = get_request(rf, plugin.request.session, {'state': 'state', 'code': 'code'})

    mocked_post = mocker.patch('rdmo.services.client.requests.post')
    mocked_post.return_value = mock_token_response(mocker, json={'access_token': 'access_token'})
    mocked_render_error = mocker.patch.object(OauthClient, 'render_error', return_value=HttpResponse())

    response = oauth_client.callback()

    # the user is not redirected to another host
    assert response.status_code == 200
    assert str(mocked_render_error.call_args.args[1]) == 'But no redirect could be found.'
