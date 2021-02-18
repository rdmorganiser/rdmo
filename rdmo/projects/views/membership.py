import logging

from django.contrib.sites.models import Site
from django.http import (HttpResponseBadRequest, HttpResponseForbidden,
                         HttpResponseRedirect)
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import DeleteView, UpdateView
from django.views.generic.edit import FormView

from rdmo.accounts.utils import is_site_manager
from rdmo.core.mail import send_mail
from rdmo.core.views import ObjectPermissionMixin, RedirectViewMixin

from ..forms import MembershipCreateForm
from ..models import Membership, Project
from ..utils import is_last_owner

logger = logging.getLogger(__name__)


class MembershipCreateView(ObjectPermissionMixin, RedirectViewMixin, FormView):
    model = Membership
    form_class = MembershipCreateForm
    permission_required = 'projects.add_membership_object'
    template_name = 'projects/membership_form.html'

    def dispatch(self, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.all(), pk=self.kwargs['project_id'])
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return Membership.objects.filter(project=self.project)

    def get_permission_object(self):
        return self.project

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.project
        kwargs['is_site_manager'] = is_site_manager(self.request.user)
        return kwargs

    def get_success_url(self):
        return self.project.get_absolute_url()

    def form_valid(self, form):
        invite = form.save()
        if invite is not None:
            context = {
                'invite_url': self.request.build_absolute_uri(reverse('project_join', args=[invite.token])),
                'invite_user': invite.user,
                'project': invite.project,
                'user': self.request.user,
                'site': Site.objects.get_current()
            }

            subject = render_to_string('projects/email/project_invite_subject.txt', context)
            message = render_to_string('projects/email/project_invite_message.txt', context)

            # send the email
            send_mail(subject, message, to=[invite.email])

        return super().form_valid(form)


class MembershipUpdateView(ObjectPermissionMixin, RedirectViewMixin, UpdateView):
    fields = ('role', )
    permission_required = 'projects.change_membership_object'

    def get_queryset(self):
        return Membership.objects.filter(project_id=self.kwargs.get('project_id'))

    def get_permission_object(self):
        return self.get_object().project


class MembershipDeleteView(ObjectPermissionMixin, RedirectViewMixin, DeleteView):
    permission_required = 'projects.delete_membership_object'

    def get_queryset(self):
        return Membership.objects.filter(project_id=self.kwargs.get('project_id'))

    def delete(self, *args, **kwargs):
        self.obj = self.get_object()

        if (self.request.user in self.obj.project.owners) or is_site_manager(self.request.user):
            # user is owner or site manager
            if is_last_owner(self.obj.project, self.obj.user):
                logger.info('User "%s" not allowed to remove last user "%s"', self.request.user.username, self.obj.user.username)
                return HttpResponseBadRequest()
            else:
                logger.info('User "%s" deletes user "%s"', self.request.user.username, self.obj.user.username)
                success_url = reverse('project', args=[self.get_object().project.id])
                self.obj.delete()
                return HttpResponseRedirect(success_url)

        elif self.request.user == self.obj.user:
            # user wants to remove him/herself
            logger.info('User "%s" deletes himself.', self.request.user.username)
            success_url = reverse('projects')
            self.obj.delete()
            return HttpResponseRedirect(success_url)

        else:
            logger.info('User "%s" not allowed to remove user "%s"', self.request.user.username, self.obj.user.username)
            return HttpResponseForbidden()

    def get_permission_object(self):
        return self.get_object().project
