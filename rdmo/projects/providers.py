import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from rdmo.core.plugins import Plugin
from rdmo.services.providers import OauthProviderMixin


class IssueProvider(Plugin):

    def send_issue(self, request, issue, integration, subject, message, attachments):
        raise NotImplementedError

    def webhook(self, request, integration):
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
                'errors': [_('The Integration is not configured correctly.')]
            }, status=200)

        return self.post(request, url, data)

    def update_issue(self, request, remote_url):
        from rdmo.projects.models import Integration, Issue, IssueResource

        # get the issue_id and integration_id from the session
        issue_id = self.pop_from_session(request, 'issue_id')
        integration_id = self.pop_from_session(request, 'integration_id')

        try:
            issue = Issue.objects.get(pk=issue_id)
            issue.status = Issue.ISSUE_STATUS_IN_PROGRESS
            issue.save()

            integration = Integration.objects.get(pk=integration_id)

            issue_resource = IssueResource(issue=issue, integration=integration, url=remote_url)
            issue_resource.save()
        except ObjectDoesNotExist:
            pass

    def post_success(self, request, response):
        # get the upstream url of the issue
        remote_url = self.get_issue_url(response)

        # update the issue in rdmo
        self.update_issue(request, remote_url)

        return HttpResponseRedirect(remote_url)

    def get_post_url(self, request, issue, integration, subject, message, attachments):
        raise NotImplementedError

    def get_post_data(self, request, issue, integration, subject, message, attachments):
        raise NotImplementedError

    def get_issue_url(self, response):
        raise NotImplementedError


class SimpleIssueProvider(OauthIssueProvider):

    add_label = _('Add Simple integration')
    send_label = _('Send to Simple')
    description = _('This integration allow the creation of issues in arbitrary Simple repositories. '
                    'The upload of attachments is not supported.')

    @property
    def fields(self):
        return [
            {
                'key': 'project_url',
                'placeholder': 'https://example.com/projects/<name>',
                'help': _('The URL of the project to send tasks to.')
            },
            {
                'key': 'secret',
                'placeholder': 'Secret (random) string',
                'help': _('The secret for a webhook to close a task (optional).'),
                'required': False,
                'secret': True
            }
        ]

    def get(self, request, url):
        raise NotImplementedError

    def post(self, request, url, json=None, files=None, multipart=None):
        raise NotImplementedError

    def webhook(self, request, integration):
        secret = integration.get_option_value('secret')
        header_signature = request.headers.get('X-Secret')
        if secret == header_signature:
            try:
                payload = json.loads(request.body.decode())
            except json.decoder.JSONDecodeError as e:
                return HttpResponse(e, status=400)

            action = payload.get('action')
            url = payload.get('url')

            try:
                issue_resource = integration.resources.get(url=url)
                if action == 'closed':
                    issue_resource.issue.status = issue_resource.issue.ISSUE_STATUS_CLOSED
                else:
                    issue_resource.issue.status = issue_resource.issue.ISSUE_STATUS_IN_PROGRESS

                issue_resource.issue.save()
            except ObjectDoesNotExist:
                pass

            return HttpResponse(status=200)

        raise Http404
