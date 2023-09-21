import logging

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import TemplateSyntaxError
from django.template.loader import render_to_string
from django.views.generic import DetailView, UpdateView

from rest_framework.reverse import reverse

from rdmo.core.mail import send_mail
from rdmo.core.utils import render_to_format
from rdmo.core.views import ObjectPermissionMixin, RedirectViewMixin
from rdmo.views.utils import ProjectWrapper

from ..forms import IssueMailForm, IssueSendForm
from ..models import Issue
from ..utils import get_value_path

logger = logging.getLogger(__name__)


class IssueDetailView(ObjectPermissionMixin, DetailView):
    permission_required = 'projects.view_issue_object'

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs.get('project_id'))

    def get_permission_object(self):
        return self.get_object().project

    def get_context_data(self, **kwargs):
        project = self.get_object().project
        conditions = self.get_object().task.conditions.all()

        sources = []
        for condition in conditions:
            sources.append({
                'source': condition.source,
                'questions': condition.source.questions.filter(questionset__section__catalog=project.catalog),
                'values': condition.source.values.filter(project=project, snapshot=None)
            })

        kwargs['project'] = project
        kwargs['sources'] = sources
        return super().get_context_data(**kwargs)


class IssueUpdateView(ObjectPermissionMixin, RedirectViewMixin, UpdateView):
    fields = ('status', )
    permission_required = 'projects.change_issue_object'

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs.get('project_id'))

    def get_permission_object(self):
        return self.get_object().project


class IssueSendView(ObjectPermissionMixin, RedirectViewMixin, DetailView):
    permission_required = 'projects.change_issue_object'
    template_name = 'projects/issue_send.html'

    def dispatch(self, *args, **kwargs):
        if not settings.PROJECT_SEND_ISSUE:
            raise Http404

        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs.get('project_id'))

    def get_permission_object(self):
        return self.get_object().project

    def get_success_url(self):
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        else:
            return self.get_object().project.get_absolute_url()

    def get_context_data(self, **kwargs):
        self.object = self.get_object()

        issue = self.object
        project = self.get_object().project
        project_url = self.request.build_absolute_uri(project.get_absolute_url())
        site = Site.objects.get_current()
        site_url = self.request.build_absolute_uri(reverse('home'))

        if 'form' not in kwargs:
            template_context = {
                'issue': issue,
                'project': project,
                'project_url': project_url,
                'site': site,
                'site_url': site_url,
                'user': self.request.user
            }
            subject = render_to_string('projects/issue_send_subject.txt', template_context, request=self.request)
            message = render_to_string('projects/issue_send_message.txt', template_context, request=self.request)

            kwargs['form'] = IssueSendForm(initial={
                'subject': subject,
                'message': message
            }, project=project)

        if 'mail_form' not in kwargs:
            kwargs['mail_form'] = IssueMailForm()

        context = super().get_context_data(**kwargs)
        context['views'] = project.views.all()
        context['integrations'] = project.integrations.all()
        return context

    def post(self, request, *args, **kwargs):
        issue = self.get_object()
        project = issue.project

        form = IssueSendForm(request.POST, project=project)
        mail_form = IssueMailForm(request.POST)

        if form.is_valid():
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')

            snapshot = project.snapshots.filter(pk=form.cleaned_data.get('snapshot')).first()
            attachments_format = form.cleaned_data.get('attachments_format')

            attachments = []
            if form.cleaned_data.get('attachments_answers'):
                title = f'{project.title}.{attachments_format}'
                response = self.render_project_answers(project, snapshot, attachments_format)
                attachments.append((title, response.content, response['content-type']))

            for view in form.cleaned_data.get('attachments_views'):
                title = f'{project.title}.{attachments_format}'
                response = self.render_project_views(project, snapshot, view, attachments_format)
                attachments.append((title, response.content, response['content-type']))

            for value in form.cleaned_data.get('attachments_files'):
                attachments.append((value.file_name, value.file.read(), value.file_type))

            integration_id = request.POST.get('integration')
            if integration_id:
                # send via integration
                try:
                    integration = project.integrations.get(pk=integration_id)
                    return integration.provider.send_issue(request, issue, integration, subject, message, attachments)
                except (ObjectDoesNotExist, AttributeError):
                    pass
            else:
                if mail_form.is_valid():
                    to_emails = [*mail_form.cleaned_data.get('recipients', []),
                                 *mail_form.cleaned_data.get('recipients_input', [])]
                    cc_emails = [request.user.email]
                    reply_to = [request.user.email]

                    # send the email
                    send_mail(subject, message, to=to_emails, cc=cc_emails, reply_to=reply_to, attachments=attachments)

                    # update issue status
                    issue.status = Issue.ISSUE_STATUS_IN_PROGRESS
                    issue.save()

                    return HttpResponseRedirect(self.get_success_url())

        return self.render_to_response(self.get_context_data(form=form, mail_form=mail_form))

    def render_project_answers(self, project, snapshot, attachments_format):
        return render_to_format(
            self.request, attachments_format, project.title, 'projects/project_answers_export.html', {
                'project': ProjectWrapper(project, snapshot),
                'format': attachments_format,
                'title': project.title,
                'resource_path': get_value_path(project, snapshot)
            }
        )

    def render_project_views(self, project, snapshot, view, attachments_format):
        try:
            rendered_view = view.render(project, snapshot)
        except TemplateSyntaxError:
            return HttpResponse()

        return render_to_format(
            self.request, attachments_format, project.title, 'projects/project_view_export.html', {
                'format': attachments_format,
                'title': project.title,
                'view': view,
                'rendered_view': rendered_view,
                'resource_path': get_value_path(project, snapshot)
            }
        )
