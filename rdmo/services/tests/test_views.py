import pytest

from django.http import HttpResponse
from django.urls import reverse

from rdmo.services.client import OauthClient

# the oauth export from testing/config/settings/base.py uses the OauthClient
session_prefix = 'plugins.projects.exports.OAuthExport.oauth'


def test_oauth_callback(db, client, mocker):
    session = client.session
    session[f'{session_prefix}.oauth_state'] = 'state'
    session.save()

    mocked_callback = mocker.patch.object(OauthClient, 'callback', return_value=HttpResponse('callback'))

    url = reverse('oauth_callback', args=['oauth'])
    response = client.get(url, {'state': 'state', 'code': 'code'})

    # the plugin with the pending authorization handles the callback
    assert response.status_code == 200
    assert response.content == b'callback'
    mocked_callback.assert_called_once()



@pytest.mark.parametrize('class_name', [
    'plugins.projects.exports.OAuthExport',
    'plugins.projects.imports.OAuthImport'
])
def test_oauth_callback_same_key(db, client, mocker, class_name):
    # the oauth export and the oauth import from testing/config/settings/base.py both use the key oauth,
    # only the plugin with the pending authorization handles the callback
    session = client.session
    session[f'{class_name}.oauth.oauth_state'] = 'state'
    session.save()

    mocked_callback = mocker.patch.object(OauthClient, 'callback', autospec=True, return_value=HttpResponse())

    url = reverse('oauth_callback', args=['oauth'])
    response = client.get(url, {'state': 'state', 'code': 'code'})

    assert response.status_code == 200
    mocked_callback.assert_called_once()

    oauth_client = mocked_callback.call_args.args[0]
    assert oauth_client.plugin.class_name == class_name

def test_oauth_callback_not_pending(db, client, mocker):
    mocked_callback = mocker.patch.object(OauthClient, 'callback')

    url = reverse('oauth_callback', args=['oauth'])
    response = client.get(url, {'state': 'state', 'code': 'code'})

    # without a started authorization, no plugin handles the callback
    assert response.status_code == 400
    mocked_callback.assert_not_called()


def test_oauth_callback_unknown_provider(db, client, mocker):
    mocked_callback = mocker.patch.object(OauthClient, 'callback')

    url = reverse('oauth_callback', args=['unknown'])
    response = client.get(url, {'state': 'state', 'code': 'code'})

    assert response.status_code == 404
    mocked_callback.assert_not_called()
