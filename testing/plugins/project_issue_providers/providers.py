import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.utils.translation import gettext_lazy as _

from rdmo.projects.providers import OauthIssueProvider


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
