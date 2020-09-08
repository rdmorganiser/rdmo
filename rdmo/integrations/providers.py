from urllib.parse import urlencode

import requests
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _


class Provider():

    def __init__(self, request):
        self.request = request

    def send_issue(self, request, issue):
        raise NotImplementedError

    def send_view(self, request, view):
        raise NotImplementedError


class OauthProvider(Provider):

    def authorize(self):
        # get random state and store in session
        state = get_random_string(length=32)
        self.set_state(state)

        url = self.authorize_url + '?' + urlencode({
            'authorize_url': self.authorize_url,
            'client_id': self.client_id,
            'redirect_url': self.request.build_absolute_uri(self.redirect_path),
            'state': state,
            'scope': self.scope,
            'foo': 'bar'
        })

        return HttpResponseRedirect(url)

    def callback(self):
        assert self.request.GET.get('state') == self.pop_state()

        url = self.token_url + '?' + urlencode({
            'token_url': self.token_url,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': self.request.GET.get('code')
        })

        response = requests.post(url, headers={
            'Accept': 'application/json'
        })

        response.raise_for_status()
        response_data = response.json()

        # store access token in session
        self.set_access_token(response_data.get('access_token'))

        url, data = self.pop_post()
        if url:
            return self.post(url, data)
        else:
            return render(self.request, 'core/error.html', {
                'title': _('Authorization successful'),
                'errors': [_('But no redirect could be found.')]
            }, status=200)

        def set_state(self, request, state):
            raise NotImplementedError

        def pop_state(self, request):
            raise NotImplementedError

        def set_access_token(self, request, access_token):
            raise NotImplementedError

        def get_access_token(self, request, access_token):
            raise NotImplementedError

        def set_post_url(self, request, post_url):
                raise NotImplementedError

        def pop_post_url(self, request):
            raise NotImplementedError

        def set_post_data(self, request, post_data):
            raise NotImplementedError

        def pop_post_data(self, request):
            raise NotImplementedError


class GitHubProvider(OauthProvider):
    key = 'github'
    title = _('GitHub')
    description = _('GitHub, Inc. is an American multinational corporation that provides hosting for software development and version control using Git.')
    send_label = _('Send to GitHub')

    authorize_url = 'https://github.com/login/oauth/authorize'
    token_url = 'https://github.com/login/oauth/access_token'

    def __init__(self, request):
        self.request = request
        self.client_id = settings.GITHUB_INTEGRATION['client_id']
        self.client_secret = settings.GITHUB_INTEGRATION['client_secret']
        self.redirect_path = reverse('oauth_callback', args=['github'])
        self.scope = 'repo'

    def send_issue(self, issue):
        url = 'https://api.github.com/repos/rdmorganiser/issue-test/issues'
        data = {
            'title': issue.task.title,
            'body': issue.task.text
        }

        # store the post url and data in the session
        self.set_post(url, data)

        # post the data to the url
        return self.post(url, data)

    def post(self, url, data):
        # get access token from the session
        access_token = self.get_access_token()
        if access_token:
            response = requests.post(url, json=data, headers={
                'Authorization': 'token {}'.format(access_token),
                'Accept': 'application/vnd.github.v3+json'
            })
            if response.status_code == 401:
                return self.authorize()
            else:
                try:
                    response.raise_for_status()
                    return HttpResponseRedirect(response.json().get('html_url'))
                except requests.HTTPError:
                    return render(self.request, 'core/error.html', {
                        'title': _('Send error'),
                        'errors': [_('Something went wrong. Please contact support.')]
                    }, status=500)

        else:
            return self.authorize()

    def set_state(self, state):
        self.request.session['github_state'] = state

    def pop_state(self):
        return self.request.session.pop('github_state', None)

    def set_access_token(self, access_token):
        self.request.session['github_access_token'] = access_token

    def get_access_token(self):
        return self.request.session.get('github_access_token', None)

    def set_post(self, post_url, post_data):
        self.request.session['github_post'] = (post_url, post_data)

    def pop_post(self):
        return self.request.session.pop('github_post', None)
