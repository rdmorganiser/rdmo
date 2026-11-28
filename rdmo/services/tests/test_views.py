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
