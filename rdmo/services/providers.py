import logging
from urllib.parse import urlencode

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

import requests

logger = logging.getLogger(__name__)


class OauthProviderMixin:

    def get(self, request, url):
        # get access token from the session
        access_token = self.get_from_session(request, 'access_token')
        if access_token:
            # if the access_token is available post to the upstream service
            logger.debug('get: %s', url)

            response = requests.get(url, headers=self.get_authorization_headers(access_token))

            if response.status_code == 401:
                logger.warn('get forbidden: %s (%s)', response.content, response.status_code)
            else:
                try:
                    response.raise_for_status()
                    return self.get_success(request, response)

                except requests.HTTPError:
                    logger.warn('get error: %s (%s)', response.content, response.status_code)

                    return render(request, 'core/error.html', {
                        'title': _('OAuth error'),
                        'errors': [_('Something went wrong: %s') % self.get_error_message(response)]
                    }, status=200)

        # if the above did not work authorize first
        self.store_in_session(request, 'request', ('get', url, {}))
        return self.authorize(request)

    def post(self, request, url, data):
        # get access token from the session
        access_token = self.get_from_session(request, 'access_token')
        if access_token:
            # if the access_token is available post to the upstream service
            logger.debug('post: %s %s', url, data)

            response = requests.post(url, json=data, headers=self.get_authorization_headers(access_token))

            if response.status_code == 401:
                logger.warn('post forbidden: %s (%s)', response.content, response.status_code)
            else:
                try:
                    response.raise_for_status()
                    return self.post_success(request, response)

                except requests.HTTPError:
                    logger.warn('post error: %s (%s)', response.content, response.status_code)

                    return render(request, 'core/error.html', {
                        'title': _('OAuth error'),
                        'errors': [_('Something went wrong: %s') % self.get_error_message(response)]
                    }, status=200)

        # if the above did not work authorize first
        self.store_in_session(request, 'request', ('post', url, data))
        return self.authorize(request)

    def authorize(self, request):
        # get random state and store in session
        state = get_random_string(length=32)
        self.store_in_session(request, 'state', state)

        url = self.authorize_url + '?' + urlencode(self.get_authorize_params(request, state))
        return HttpResponseRedirect(url)

    def callback(self, request):
        if request.GET.get('state') != self.pop_from_session(request, 'state'):
            return render(request, 'core/error.html', {
                'title': _('OAuth authorization not successful'),
                'errors': [_('State parameter did not match.')]
            }, status=200)

        url = self.token_url + '?' + urlencode(self.get_callback_params(request))

        response = requests.post(url, self.get_callback_data(request),
                                 auth=self.get_callback_auth(request),
                                 headers=self.get_callback_headers(request))

        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            logger.error('callback error: %s (%s)', response.content, response.status_code)
            raise e

        response_data = response.json()

        # store access token in session
        self.store_in_session(request, 'access_token', response_data.get('access_token'))

        # get post data from session
        try:
            method, url, data = self.pop_from_session(request, 'request')
            if method == 'get':
                return self.get(request, url)
            elif method == 'post':
                return self.post(request, url, data)
        except ValueError:
            pass

        return render(request, 'core/error.html', {
            'title': _('OAuth authorization successful'),
            'errors': [_('But no redirect could be found.')]
        }, status=200)

    def get_success(self, request, response):
        raise NotImplementedError

    def post_success(self, request, response):
        raise NotImplementedError

    def get_session_key(self, key):
        return f'{self.class_name}.{key}'

    def store_in_session(self, request, key, data):
        session_key = self.get_session_key(key)
        request.session[session_key] = data

    def get_from_session(self, request, key):
        session_key = self.get_session_key(key)
        return request.session.get(session_key, None)

    def pop_from_session(self, request, key):
        session_key = self.get_session_key(key)
        return request.session.pop(session_key, None)

    def get_authorization_headers(self, access_token):
        return {'Authorization': f'Bearer {access_token}'}

    def get_authorize_params(self, request, state):
        raise NotImplementedError

    def get_callback_auth(self, request):
        return None

    def get_callback_headers(self, request):
        return {'Accept': 'application/json'}

    def get_callback_params(self, request):
        return {}

    def get_callback_data(self, request):
        return {}

    def get_error_message(self, response):
        return response.json().get('error')


class GitHubProviderMixin(OauthProviderMixin):
    authorize_url = 'https://github.com/login/oauth/authorize'
    token_url = 'https://github.com/login/oauth/access_token'
    api_url = 'https://api.github.com'

    @property
    def client_id(self):
        return settings.GITHUB_PROVIDER['client_id']

    @property
    def client_secret(self):
        return settings.GITHUB_PROVIDER['client_secret']

    @property
    def redirect_path(self):
        return reverse('oauth_callback', args=['github'])

    def get_authorization_headers(self, access_token):
        return {
            'Authorization': f'token {access_token}',
            'Accept': 'application/vnd.github.v3+json'
        }

    def get_authorize_params(self, request, state):
        return {
            'authorize_url': self.authorize_url,
            'client_id': self.client_id,
            'redirect_uri': request.build_absolute_uri(self.redirect_path),
            'scope': 'repo',
            'state': state,
        }

    def get_callback_params(self, request):
        return {
            'token_url': self.token_url,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': request.GET.get('code')
        }


class GitLabProviderMixin(OauthProviderMixin):

    @property
    def gitlab_url(self):
        return settings.GITLAB_PROVIDER['gitlab_url'].strip('/')

    @property
    def authorize_url(self):
        return f'{self.gitlab_url}/oauth/authorize'

    @property
    def token_url(self):
        return f'{self.gitlab_url}/oauth/token'

    @property
    def api_url(self):
        return f'{self.gitlab_url}/api/v4'

    @property
    def client_id(self):
        return settings.GITLAB_PROVIDER['client_id']

    @property
    def client_secret(self):
        return settings.GITLAB_PROVIDER['client_secret']

    @property
    def redirect_path(self):
        return reverse('oauth_callback', args=['gitlab'])

    def get_authorize_params(self, request, state):
        return {
            'authorize_url': self.authorize_url,
            'client_id': self.client_id,
            'redirect_uri': request.build_absolute_uri(self.redirect_path),
            'response_type': 'code',
            'scope': 'api',
            'state': state,
        }

    def get_callback_params(self, request):
        return {
            'token_url': self.token_url,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': request.GET.get('code'),
            'grant_type': 'authorization_code',
            'redirect_uri': request.build_absolute_uri(self.redirect_path)
        }
