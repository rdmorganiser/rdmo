import hmac
import json
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _
from rdmo.core.plugins import Plugin


class Provider(Plugin):

    def send_issue(self, request, issue, integration, subject, message, attachments):
        raise NotImplementedError

    def webhook(self, request, options, payload):
        raise NotImplementedError


class OauthProvider(Provider):

    def authorize(self, request):
        # get random state and store in session
        state = get_random_string(length=32)
        self.store_in_session(request, 'state', state)

        url = self.authorize_url + '?' + urlencode({
            'authorize_url': self.authorize_url,
            'client_id': self.client_id,
            'redirect_uri': request.build_absolute_uri(self.redirect_path),
            'state': state,
            'scope': self.scope
        })

        return HttpResponseRedirect(url)

    def callback(self, request):
        assert request.GET.get('state') == self.pop_from_session(request, 'state')

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
        self.store_in_session(request, 'access_token', response_data.get('access_token'))

        # get post data from session
        try:
            url, data, issue_id, integration_id = self.pop_from_session(request, 'post')
            return self.post(request, url, data, issue_id, integration_id)
        except ValueError:
            return render(request, 'core/error.html', {
                'title': _('Authorization successful'),
                'errors': [_('But no redirect could be found.')]
            }, status=200)

    def get_session_key(self, key):
        class_name = self.__class__.__name__.lower()
        return '{}_{}'.format(class_name, key)

    def store_in_session(self, request, key, data):
        session_key = self.get_session_key(key)
        request.session[session_key] = data

    def get_from_session(self, request, key):
        session_key = self.get_session_key(key)
        return request.session.get(session_key, None)

    def pop_from_session(self, request, key):
        session_key = self.get_session_key(key)
        return request.session.pop(session_key, None)


class GitHubProvider(OauthProvider):
    add_label = _('Add GitHub integration')
    send_label = _('Send to GitHub')
    description = _('This integration allow the creation of issues in arbitrary GitHub repositories. The upload of attachments is not supported by GitHub.')

    authorize_url = 'https://github.com/login/oauth/authorize'
    token_url = 'https://github.com/login/oauth/access_token'

    client_id = settings.GITHUB_PROVIDER['client_id']
    client_secret = settings.GITHUB_PROVIDER['client_secret']
    redirect_path = reverse('oauth_callback', args=['github'])
    scope = 'repo'

    def send_issue(self, request, issue, integration, subject, message, attachments):
        try:
            repo = integration.options.get(key='repo').value
        except ObjectDoesNotExist:
            return render(request, 'core/error.html', {
                'title': _('Integration error'),
                'errors': [_('The Integration is not configured correctly.') % message]
            }, status=200)

        url = 'https://api.github.com/repos/{}/issues'.format(repo)
        data = {
            'title': subject,
            'body': message
        }

        return self.post(request, url, data, issue.id, integration.id)

    def post(self, request, url, data, issue_id, integration_id):
        # get access token from the session
        access_token = self.get_from_session(request, 'access_token')

        if access_token:
            response = requests.post(url, json=data, headers={
                'Authorization': 'token {}'.format(access_token),
                'Accept': 'application/vnd.github.v3+json'
            })
            if response.status_code == 401:
                pass
            else:
                try:
                    response.raise_for_status()
                    response_html_url = response.json().get('html_url')
                    self._update_issue(issue_id, integration_id, response_html_url)
                    return HttpResponseRedirect(response_html_url)
                except requests.HTTPError:
                    message = response.json().get('message')
                    return render(request, 'core/error.html', {
                        'title': _('Send error'),
                        'errors': [_('Something went wrong. GitHub replied: %s.') % message]
                    }, status=200)

        # if the above did not work authorize first
        self.store_in_session(request, 'post', (url, data, issue_id, integration_id))
        return self.authorize(request)

    def _update_issue(self, issue_id, integration_id, resource_url):
        from rdmo.projects.models import Issue, Integration, IssueResource
        try:
            issue = Issue.objects.get(pk=issue_id)
            issue.status = Issue.ISSUE_STATUS_IN_PROGRESS
            issue.save()

            integration = Integration.objects.get(pk=integration_id)

            issue_resource = IssueResource(issue=issue, integration=integration, url=resource_url)
            issue_resource.save()
        except ObjectDoesNotExist:
            pass

    def webhook(self, request, integration):
        try:
            secret = integration.options.get(key='secret').value
        except ObjectDoesNotExist:
            raise Http404

        header_signature = request.headers.get('X-Hub-Signature')
        if header_signature:
            body_signature = 'sha1=' + hmac.new(secret.encode(), request.body, 'sha1').hexdigest()

            if hmac.compare_digest(header_signature, body_signature):
                try:
                    payload = json.loads(request.body.decode())
                    action = payload.get('action')
                    issue_url = payload.get('issue', {}).get('html_url')

                    if action and issue_url:
                        try:
                            issue_resource = integration.resources.get(url=issue_url)
                            if action == 'closed':
                                issue_resource.issue.status = issue_resource.issue.ISSUE_STATUS_CLOSED
                            else:
                                issue_resource.issue.status = issue_resource.issue.ISSUE_STATUS_IN_PROGRESS

                            issue_resource.issue.save()
                        except ObjectDoesNotExist:
                            pass

                    return HttpResponse(status=200)

                except json.decoder.JSONDecodeError as e:
                    return HttpResponse(e, status=400)

        raise Http404

    @property
    def fields(self):
        return [
            {
                'key': 'repo',
                'placeholder': 'user_name/repo_name',
                'help': _('The GitHub repository to send issues to.')
            },
            {
                'key': 'secret',
                'placeholder': 'Secret (random) string',
                'help': _('The secret for a GitHub webhook to close a task.'),
                'required': False,
                'secret': True
            }
        ]
