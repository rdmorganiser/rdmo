from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from rdmo.core.plugins import Plugin
from rdmo.services.providers import OauthProviderMixin


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
