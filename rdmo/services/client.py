import logging
import time
from urllib.parse import urlencode

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import gettext_lazy as _

from rest_framework.response import Response

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

from rdmo.core.plugins import PluginSession

from .exceptions import OauthAuthorizationRequired

logger = logging.getLogger(__name__)


class OauthClient:
    '''
    OAuth 2.0 client (authorization code flow) for a plugin, used similar to the PluginSession.
    The configuration is given when the client is created:

        class ExampleExport(Export):

            @property
            def client(self):
                return OauthClient(
                    self,
                    authorize_url='https://example.com/oauth/authorize',
                    token_url='https://example.com/oauth/token',
                    client_id=settings.EXAMPLE_PROVIDER['client_id'],
                    client_secret=settings.EXAMPLE_PROVIDER['client_secret'],
                    scope='write'
                )

            def submit(self):
                try:
                    response = self.client.post(url, json=data)
                except OauthAuthorizationRequired:
                    return self.client.redirect(next_url)
                ...

    The client stores its state (state, access and refresh token, next url) in the session of the plugin,
    so the plugin needs to have a request. After the authorization, the callback redirects to
    the next url given to authorize, where the plugin can repeat the request.
    '''

    def __init__(self, plugin, authorize_url, token_url, client_id, client_secret, scope=None, timeout=30):
        self.plugin = plugin
        self.authorize_url = authorize_url
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.timeout = timeout

    @property
    def session(self):
        return PluginSession(self.plugin)

    @property
    def request(self):
        return self.plugin.request

    @property
    def access_token(self):
        return self.session.get('oauth_access_token')

    @property
    def refresh_token(self):
        return self.session.get('oauth_refresh_token')

    def is_expired(self):
        # the access token is considered expired a bit earlier, to account for the time of the request
        expires_at = self.session.get('oauth_expires_at')
        return expires_at is not None and time.time() > expires_at - 30

    @property
    def redirect_uri(self):
        return self.request.build_absolute_uri(reverse('oauth_callback', args=[self.plugin.key]))

    def is_pending(self):
        # an authorization was started for this plugin, but the callback did not happen yet
        return self.session.get('oauth_state') is not None

    def get(self, url, **kwargs):
        return self.send('get', url, **kwargs)

    def post(self, url, **kwargs):
        return self.send('post', url, **kwargs)

    def put(self, url, **kwargs):
        return self.send('put', url, **kwargs)

    def delete(self, url, **kwargs):
        return self.send('delete', url, **kwargs)

    def upload(self, url, files, data=None, method='post', **kwargs):
        # upload files as multipart/form-data, files maps the field names to tuples of
        # (file_name, file_or_bytes, content_type), data contains additional form fields
        return self.send(method, url, multipart={**(data or {}), **files}, **kwargs)

    def send(self, method, url, **kwargs):
        # send a request to the upstream service, the kwargs are passed to requests,
        # raises OauthAuthorizationRequired if there is no (valid) access token,
        # and it could not be renewed using the refresh token
        if (not self.access_token or self.is_expired()) and not self.refresh():
            raise OauthAuthorizationRequired

        response = self.send_request(method, url, **kwargs)

        if response.status_code == 401:
            # the access token is not valid anymore, try once more with a refreshed token
            logger.warning('%s unauthorized: %s (%s)', method, response.content, response.status_code)

            if not self.refresh():
                raise OauthAuthorizationRequired

            response = self.send_request(method, url, **kwargs)

            if response.status_code == 401:
                logger.warning('%s unauthorized: %s (%s)', method, response.content, response.status_code)
                self.clear_token()
                raise OauthAuthorizationRequired

        return response

    def send_request(self, method, url, **kwargs):
        logger.debug('%s: %s', method, url)

        headers = {**self.get_authorization_headers(), **kwargs.pop('headers', {})}
        kwargs.setdefault('timeout', self.timeout)

        multipart = kwargs.pop('multipart', None)
        if multipart is not None:
            # the encoder is consumed by the request, so it is created for every attempt,
            # and files are rewound, so that the request can be repeated after a refresh
            for value in multipart.values():
                file = value[1] if isinstance(value, tuple) else value
                if hasattr(file, 'seek'):
                    file.seek(0)

            encoder = MultipartEncoder(fields=multipart)
            headers['Content-Type'] = encoder.content_type
            kwargs['data'] = encoder

        return requests.request(method, url, headers=headers, **kwargs)

    def refresh(self):
        # renew the access token using the refresh token, returns True if successful
        if not self.refresh_token:
            self.clear_token()
            return False

        response = self.request_token(self.get_refresh_data(self.refresh_token))

        try:
            response.raise_for_status()
        except requests.HTTPError:
            logger.warning('refresh error: %s (%s)', response.content, response.status_code)
            self.clear_token()
            return False

        self.store_token(response.json())
        return True

    def request_token(self, data):
        return requests.post(
            self.token_url,
            data=data,
            auth=self.get_token_auth(),
            headers=self.get_token_headers(),
            timeout=self.timeout
        )

    def store_token(self, token_data):
        self.session.set('oauth_access_token', token_data.get('access_token'))

        # some providers do not return a new refresh token, in this case the old one is kept
        if token_data.get('refresh_token'):
            self.session.set('oauth_refresh_token', token_data.get('refresh_token'))

        if token_data.get('expires_in'):
            self.session.set('oauth_expires_at', time.time() + int(token_data.get('expires_in')))
        else:
            self.session.pop('oauth_expires_at')

    def clear_token(self):
        for key in ['oauth_access_token', 'oauth_refresh_token', 'oauth_expires_at']:
            self.session.pop(key)

    def authorize(self, next_url):
        # store a random state and the url to return to after the callback,
        # and return the url to redirect the user to for the authorization
        state = get_random_string(length=32)
        self.session.set('oauth_state', state)
        self.session.set('oauth_next', next_url)

        return self.authorize_url + '?' + urlencode(self.get_authorize_params(state))

    def redirect(self, next_url):
        # return a response, which tells the frontend to redirect to the authorize url
        return Response({'redirect_url': self.authorize(next_url)})

    def callback(self):
        # handle the redirect from the authorization server
        if self.request.GET.get('state') != self.session.pop('oauth_state'):
            return self.render_error(_('OAuth authorization not successful'), _('State parameter did not match.'))

        if 'error' in self.request.GET:
            return self.render_error(_('OAuth authorization not successful'), self.request.GET.get('error'))

        response = self.request_token(self.get_token_data(self.request.GET.get('code')))

        try:
            response.raise_for_status()
        except requests.HTTPError:
            logger.error('callback error: %s (%s)', response.content, response.status_code)
            return self.render_error(_('OAuth error'), self.get_error_message(response))

        self.store_token(response.json())

        next_url = self.session.pop('oauth_next')
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={self.request.get_host()}):
            return HttpResponseRedirect(next_url)

        return self.render_error(_('OAuth authorization successful'), _('But no redirect could be found.'))

    def render_error(self, title, error):
        return render(self.request, 'core/error.html', {
            'title': title,
            'errors': [error]
        }, status=200)

    def get_authorization_headers(self):
        return {'Authorization': f'Bearer {self.access_token}'}

    def get_authorize_params(self, state):
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'state': state
        }
        if self.scope:
            params['scope'] = self.scope
        return params

    def get_token_data(self, code):
        return {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

    def get_refresh_data(self, refresh_token):
        return {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

    def get_token_auth(self):
        return None

    def get_token_headers(self):
        return {'Accept': 'application/json'}

    def get_error_message(self, response):
        try:
            return response.json().get('error')
        except ValueError:
            return response.reason
