import hmac
import json
from urllib.parse import quote

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from rdmo.core.plugins import Plugin
from rdmo.services.providers import (
    GitHubProviderMixin,
    GitLabProviderMixin,
    OauthProviderMixin,
    OpenProjectProviderMixin,
)


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


class GitHubIssueProvider(GitHubProviderMixin, OauthIssueProvider):
    add_label = _('Add GitHub integration')
    send_label = _('Send to GitHub')
    description = _('This integration allow the creation of issues in arbitrary GitHub repositories. '
                    'The upload of attachments is not supported by GitHub.')

    def get_post_url(self, request, issue, integration, subject, message, attachments):
        repo = integration.get_option_value('repo')
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
        secret = integration.get_option_value('secret')
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
                'help': _('The secret for a GitHub webhook to close a task (optional).'),
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

    def get_post_url(self, request, issue, integration, subject, message, attachments):
        repo = integration.get_option_value('repo')
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
        secret = integration.get_option_value('secret')
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
                'help': _('The secret for a GitLab webhook to close a task (optional).'),
                'required': False,
                'secret': True
            }
        ]


class OpenProjectIssueProvider(OpenProjectProviderMixin, OauthIssueProvider):
    add_label = _('Add OpenProject integration')
    send_label = _('Send to OpenProject')

    status_map = {
        'New': 'open',
        'To be scheduled': 'in_progress',
        'Scheduled': 'in_progress',
        'In progress': 'in_progress',
        'Closed': 'closed',
        'On hold': 'in_progress',
        'Rejected': 'closed'
    }

    @property
    def description(self):
        return _(f'This integration allow the creation of issues on {self.openproject_url}.')

    def send_issue(self, request, issue, integration, subject, message, attachments):
        self.store_in_session(request, 'issue_id', issue.id)
        self.store_in_session(request, 'integration_id', integration.id)
        self.store_in_session(request, 'project_name', integration.get_option_value('project_name'))
        self.store_in_session(request, 'work_package_type', integration.get_option_value('work_package_type'))
        self.store_in_session(request, 'subject', subject)
        self.store_in_session(request, 'message', message)
        self.store_in_session(request, 'attachments', attachments)

        return self.get_project_id(request)

    def get_project_id(self, request):
        project_name = self.pop_from_session(request, 'project_name')
        query = quote(json.dumps([{
            'name_and_identifier': {
                'operator': '=',
                'values': [project_name]
            }
        }]))
        url = f'{self.api_url}/projects?filters={query}'

        return self.get(request, url)

    def get_type_id(self, request):
        url = f'{self.api_url}/types'
        return self.get(request, url)

    def post_issue(self, request):
        project_id = self.get_from_session(request, 'project_id')
        type_id = self.get_from_session(request, 'type_id')
        url = f'{self.api_url}/projects/{project_id}/work_packages'
        data = {
            '_links': {
                'type': {
                    'href': f'/api/v3/types/{type_id}'
                }
            },
            'subject': self.pop_from_session(request, 'subject'),
            'description': {
                'format': 'plain',
                'raw': self.pop_from_session(request, 'message'),
            }
        }

        return self.post(request, url, data)

    def post_attachment(self, request):
        work_package_id = self.get_from_session(request, 'work_package_id')
        attachments = self.pop_from_session(request, 'attachments')

        if attachments:
            file_name, file_content, file_type = attachments[0]
            url = f'{self.api_url}/work_packages/{work_package_id}/attachments'
            multipart = {
                'metadata': json.dumps({'fileName': file_name }),
                'file': (file_name, file_content, file_type)
            }

            self.store_in_session(request, 'attachments', attachments[1:])
            return self.post(request, url, multipart=multipart)

        else:
            # there are no attachments left, get the url of the work_package
            remote_url = self.get_work_package_url(work_package_id)

            # update the issue in rdmo
            self.update_issue(request, remote_url)

            # redirect to the work package in open project
            return HttpResponseRedirect(remote_url)

    def get_success(self, request, response):
        if '/projects' in response.url:
            try:
                project_id = response.json()['_embedded']['elements'][0]['id']
                self.store_in_session(request, 'project_id', project_id)
                return self.get_type_id(request)

            except (KeyError, IndexError):
                return render(request, 'core/error.html', {
                    'title': _('Integration error'),
                    'errors': [_('OpenProject project could not be found.')]
                }, status=200)

        elif '/types' in response.url:
            try:
                work_package_type = self.pop_from_session(request, 'work_package_type')
                for element in response.json()['_embedded']['elements']:
                    if element['name'] == work_package_type:
                        self.store_in_session(request, 'type_id', element['id'])
                        return self.post_issue(request)

            except KeyError:
                pass

            return render(request, 'core/error.html', {
                'title': _('Integration error'),
                'errors': [_('OpenProject work package type could not be found.')]
            }, status=200)

        elif response.request.method == 'POST':
            pass

        # return an error if everything failed
        return render(request, 'core/error.html', {
            'title': _('Integration error'),
            'errors': [_('The Integration is not configured correctly.')]
        }, status=200)

    def post_success(self, request, response):
        if '/projects/' in response.url:
            # get the upstream url of the issue
            work_package_id = response.json()['id']
            self.store_in_session(request, 'work_package_id', work_package_id)

        # post the next attachment
        return self.post_attachment(request)

    def get_work_package_url(self, work_package_id):
        return f'{self.openproject_url}/work_packages/{work_package_id}'

    def webhook(self, request, integration):
        secret = integration.get_option_value('secret')
        header_signature = request.headers.get('X-Op-Signature')

        if (secret is not None) and (header_signature is not None):
            body_signature = 'sha1=' + hmac.new(secret.encode(), request.body, 'sha1').hexdigest()

            if hmac.compare_digest(header_signature, body_signature):
                try:
                    payload = json.loads(request.body.decode())
                    action = payload.get('action')
                    work_package = payload.get('work_package')

                    if action and work_package:
                        work_package_id = work_package.get('id')
                        work_package_url = self.get_work_package_url(work_package_id)
                        work_package_status = work_package.get('_links', {}).get('status', {}).get('title')

                        try:
                            issue_resource = integration.resources.get(url=work_package_url)
                            status_map = self.status_map
                            status_map.update(settings.OPENPROJECT_PROVIDER.get('status_map', {}))

                            if work_package_status in status_map:
                                print('-->' , status_map[work_package_status])
                                issue_resource.issue.status = status_map[work_package_status]
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
                'key': 'project_name',
                'placeholder': 'Project',
                'help': _('The name of the OpenProject url')
            },
            {
                'key': 'work_package_type',
                'placeholder': 'Work Package Type',
                'help': _('The type of workpackage to create, e.g. "Task"')
            },
            {
                'key': 'secret',
                'placeholder': 'Secret (random) string',
                'help': _('The secret for a OpenProject webhook to close a task (optional).'),
                'required': False,
                'secret': True
            }
        ]
