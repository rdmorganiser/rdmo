import hmac
import json
from urllib.parse import quote

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from rdmo.core.plugins import Plugin
from rdmo.services.providers import GitHubProviderMixin, GitLabProviderMixin, OauthProviderMixin


class IssueProvider(Plugin):

    def send_issue(self, request, issue, integration, subject, message, attachments):
        raise NotImplementedError

    def webhook(self, request, options, payload):
        raise NotImplementedError


class OauthIssueProvider(OauthProviderMixin, IssueProvider):

    def send_issue(self, request, issue, integration, subject, message, attachments):
        url = self.get_post_url(request, issue, integration, subject, message, attachments)
        data = self.get_post_data(request, issue, integration, subject, message, attachments)

        self.store_in_session(request, 'issue_id', issue.id)
        self.store_in_session(request, 'integration_id', integration.id)

        if url is None or data is None:
            return render(request, 'core/error.html', {
                'title': _('Integration error'),
                'errors': [_('The Integration is not configured correctly.') % message]
            }, status=200)

        return self.post(request, url, data)

    def post_success(self, request, response):
        from rdmo.projects.models import Integration, Issue, IssueResource

        # get the upstream url of the issue
        remote_url = self.get_issue_url(response)

        # get the issue_id and integration_id from the session
        issue_id = self.pop_from_session(request, 'issue_id')
        integration_id = self.pop_from_session(request, 'integration_id')

        # update the issue in rdmo
        try:
            issue = Issue.objects.get(pk=issue_id)
            issue.status = Issue.ISSUE_STATUS_IN_PROGRESS
            issue.save()

            integration = Integration.objects.get(pk=integration_id)

            issue_resource = IssueResource(issue=issue, integration=integration, url=remote_url)
            issue_resource.save()
        except ObjectDoesNotExist:
            pass

        return HttpResponseRedirect(remote_url)

    def get_post_url(self, request, issue, integration, subject, message, attachments):
        raise NotImplementedError

    def get_post_data(self, request, issue, integration, subject, message, attachments):
        raise NotImplementedError

    def get_issue_url(self, response):
        raise NotImplementedError


class GitHubIssueProvider(GitHubProviderMixin, OauthIssueProvider):
    add_label = _('Add GitHub integration')
    send_label = _('Send to GitHub')
    description = _('This integration allow the creation of issues in arbitrary GitHub repositories. '
                    'The upload of attachments is not supported by GitHub.')

    def get_repo(self, integration):
        try:
            return integration.options.get(key='repo').value
        except ObjectDoesNotExist:
            return None

    def get_secret(self, integration):
        try:
            return integration.options.get(key='secret').value
        except ObjectDoesNotExist:
            return None

    def get_post_url(self, request, issue, integration, subject, message, attachments):
        repo = self.get_repo(integration)
        if repo:
            return f'https://api.github.com/repos/{repo}/issues'

    def get_post_data(self, request, issue, integration, subject, message, attachments):
        return {
            'title': subject,
            'body': message
        }

    def get_issue_url(self, response):
        return response.json().get('html_url')

    def webhook(self, request, integration):
        secret = self.get_secret(integration)
        header_signature = request.headers.get('X-Hub-Signature')

        if (secret is not None) and (header_signature is not None):
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


class GitLabIssueProvider(GitLabProviderMixin, OauthIssueProvider):
    add_label = _('Add GitLab integration')
    send_label = _('Send to GitLab')

    @property
    def description(self):
        return _(f'This integration allow the creation of issues in arbitrary repositories on {self.gitlab_url}. '
                 'The upload of attachments is not supported by GitLab.')

    def get_repo(self, integration):
        try:
            return integration.options.get(key='repo').value
        except ObjectDoesNotExist:
            return None

    def get_secret(self, integration):
        try:
            return integration.options.get(key='secret').value
        except ObjectDoesNotExist:
            return None

    def get_post_url(self, request, issue, integration, subject, message, attachments):
        repo = self.get_repo(integration)
        if repo:
            return '{}/api/v4/projects/{}/issues'.format(self.gitlab_url, quote(repo, safe=''))

    def get_post_data(self, request, issue, integration, subject, message, attachments):
        return {
            'title': subject,
            'description': message
        }

    def get_issue_url(self, response):
        return response.json().get('web_url')

    def webhook(self, request, integration):
        secret = self.get_secret(integration)
        header_token = request.headers.get('X-Gitlab-Token')

        if (secret is not None) and (header_token is not None) and (header_token == secret):
            try:
                payload = json.loads(request.body.decode())
                state = payload.get('object_attributes', {}).get('state')
                issue_url = payload.get('object_attributes', {}).get('url')

                if state and issue_url:
                    try:
                        issue_resource = integration.resources.get(url=issue_url)
                        if state == 'closed':
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
                'help': _('The GitLab repository to send issues to.')
            },
            {
                'key': 'secret',
                'placeholder': 'Secret (random) string',
                'help': _('The secret for a GitLab webhook to close a task.'),
                'required': False,
                'secret': True
            }
        ]
