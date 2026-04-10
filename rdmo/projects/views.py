import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import DetailView, TemplateView

from rdmo.core.views import CSRFViewMixin, ObjectPermissionMixin, RedirectViewMixin, StoreIdViewMixin

from .models import Invite, Membership, Project

logger = logging.getLogger(__name__)


class ProjectsView(LoginRequiredMixin, CSRFViewMixin, StoreIdViewMixin, TemplateView):
    template_name = 'projects/projects.html'


class ProjectDetailView(ObjectPermissionMixin, CSRFViewMixin, StoreIdViewMixin, DetailView):
    model = Project
    permission_required = 'projects.view_project_object'


class ProjectJoinView(LoginRequiredMixin, RedirectViewMixin, TemplateView):
    template_name = 'core/error.html'

    def get(self, request, token):
        try:
            invite = Invite.objects.get(token=token)

            if invite.is_expired:
                error = _('Sorry, your invitation has been expired.')
                invite.delete()
            elif invite.user and invite.user != request.user:
                error = _('Sorry, but this invitation is for the user "%s".') % invite.user
            elif Membership.objects.filter(project=invite.project, user=request.user).exists():
                invite.delete()
                return redirect(invite.project.get_absolute_url())
            else:
                Membership.objects.create(
                    project=invite.project,
                    user=request.user,
                    role=invite.role
                )
                invite.delete()
                return redirect(invite.project.get_absolute_url())

        except Invite.DoesNotExist:
            error = _('Sorry, the invitation link is not valid.')

        return self.render_to_response({
            'title': _('Error'),
            'errors': [error]
        })


class ProjectInterviewView(ObjectPermissionMixin, CSRFViewMixin, StoreIdViewMixin, DetailView):
    model = Project
    queryset = Project.objects.all()
    permission_required = 'projects.view_project_object'
    template_name = 'projects/project_interview.html'

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.catalog is None:
            return redirect('project_error', pk=self.object.pk)
        else:
            return super().get(request, *args, **kwargs)


class ProjectErrorView(ObjectPermissionMixin, DetailView):
    model = Project
    queryset = Project.objects.all()
    permission_required = 'projects.view_project_object'
    template_name = 'projects/project_error.html'
