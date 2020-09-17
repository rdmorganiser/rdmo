import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, UpdateView
from rdmo.core.views import ObjectPermissionMixin, RedirectViewMixin

from ..forms import IssueMailForm, IssueSendForm
from ..models import Issue

logger = logging.getLogger(__name__)


class IssueUpdateView(ObjectPermissionMixin, RedirectViewMixin, UpdateView):
    model = Issue
    queryset = Issue.objects.all()
    fields = ('status', )
    permission_required = 'projects.change_issue_object'

    def get_permission_object(self):
        return self.get_object().project


class IssueSendView(ObjectPermissionMixin, RedirectViewMixin, DetailView):
    queryset = Issue.objects.all()
    permission_required = 'projects.change_issue_object'
    template_name = 'projects/issue_send.html'

    def get_permission_object(self):
        return self.get_object().project

    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs['form'] = IssueSendForm(initial={
                'subject': self.object.task.title,
                'message': self.object.task.text
            })

        if 'mail_form' not in kwargs:
            kwargs['mail_form'] = IssueMailForm()

        context = super().get_context_data(**kwargs)
        context['integrations'] = self.get_object().project.integrations.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.status = Issue.ISSUE_STATUS_IN_PROGRESS
        self.object.save()

        form = IssueSendForm(request.POST)
        mail_form = IssueMailForm(request.POST)

        if form.is_valid():
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')

            integration_id = request.POST.get('integration')
            if integration_id:
                # send via integration
                integration = self.get_object().project.integrations.get(pk=integration_id)
                return integration.provider.send(request, integration.options_dict, subject, message)
            else:
                if mail_form.is_valid():
                    from_email = settings.DEFAULT_FROM_EMAIL
                    to_emails = mail_form.cleaned_data.get('recipients', []) + mail_form.cleaned_data.get('recipients_input', [])
                    cc_emails = [request.user.email]
                    reply_to = [request.user.email]

                    EmailMessage(subject, message, from_email, to_emails, cc=cc_emails, reply_to=reply_to).send()
                    return HttpResponseRedirect(self.get_object().project.get_absolute_url())

        return self.render_to_response(self.get_context_data(form=form, mail_form=mail_form))
