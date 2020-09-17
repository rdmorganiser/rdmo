from urllib.parse import urlencode

import requests
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _


class Provider():

    def send(self, request, options, subject, message):
        raise NotImplementedError


class OauthProvider(Provider):

    def authorize(self, request):
        # get random state and store in session
        state = get_random_string(length=32)
        self.set_state(request, state)

        url = self.authorize_url + '?' + urlencode({
            'authorize_url': self.authorize_url,
            'client_id': self.client_id,
            'redirect_url': request.build_absolute_uri(self.redirect_path),
            'state': state,
            'scope': self.scope,
            'foo': 'bar'
        })

        return HttpResponseRedirect(url)

    def callback(self, request):
        assert request.GET.get('state') == self.pop_state(request)

        url = self.token_url + '?' + urlencode({
            'token_url': self.token_url,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': request.GET.get('code')
        })

        response = requests.post(url, headers={
            'Accept': 'application/json'
        })

        response.raise_for_status()
        response_data = response.json()

        # store access token in session
        self.set_access_token(request, response_data.get('access_token'))

        url, data = self.pop_post(request)
        if url:
            return self.post(request, url, data)
        else:
            return render(request, 'core/error.html', {
                'title': _('Authorization successful'),
                'errors': [_('But no redirect could be found.')]
            }, status=200)

    def get_session_key(self, key):
        class_name = self.__class__.__name__.lower()
        return '{}_{}'.format(class_name, key)

    def set_state(self, request, state):
        session_key = self.get_session_key('state')
        request.session[session_key] = state

    def pop_state(self, request):
        session_key = self.get_session_key('state')
        return request.session.pop(session_key, None)

    def set_access_token(self, request, access_token):
        session_key = self.get_session_key('access_token')
        request.session[session_key] = access_token

    def get_access_token(self, request):
        session_key = self.get_session_key('access_token')
        return request.session.get(session_key, None)

    def set_post(self, request, post_url, post_data):
        session_key = self.get_session_key('post')
        request.session[session_key] = (post_url, post_data)

    def pop_post(self, request):
        session_key = self.get_session_key('post')
        return request.session.pop(session_key, None)


class GitHubProvider(OauthProvider):
    title = _('GitHub')
    description = _('GitHub, Inc. is an American multinational corporation that provides hosting for software development and version control using Git.')
    list_label = _('GitHub integration')
    add_label = _('Add GitHub integration')
    send_label = _('Send to GitHub')

    authorize_url = 'https://github.com/login/oauth/authorize'
    token_url = 'https://github.com/login/oauth/access_token'

    client_id = settings.GITHUB_PROVIDER['client_id']
    client_secret = settings.GITHUB_PROVIDER['client_secret']
    redirect_path = reverse('oauth_callback', args=['github'])
    scope = 'repo'

    def send(self, request, options, subject, message):
        url = 'https://api.github.com/repos/{}/issues'.format(options.get('repo'))
        data = {
            'title': subject,
            'body': message
        }

        # store the post url and data in the session
        self.set_post(request, url, data)

        # post the data to the url
        return self.post(request, url, data)

    def post(self, request, url, data):
        # get access token from the session
        access_token = self.get_access_token(request)
        if access_token:
            response = requests.post(url, json=data, headers={
                'Authorization': 'token {}'.format(access_token),
                'Accept': 'application/vnd.github.v3+json'
            })
            if response.status_code == 401:
                return self.authorize(request)
            else:
                try:
                    response.raise_for_status()
                    return HttpResponseRedirect(response.json().get('html_url'))
                except requests.HTTPError:
                    message = response.json().get('message')
                    return render(request, 'core/error.html', {
                        'title': _('Send error'),
                        'errors': [_('Something went wrong. GitHub replied: %s.') % message]
                    }, status=500)

        else:
            return self.authorize(request)

    @property
    def fields(self):
        return [
            {
                'key': 'repo',
                'placeholder': 'user_name/repo_name',
                'help': _('The repository to send issues to, e.g. rdmorganiser/rdmo')
            }
        ]
