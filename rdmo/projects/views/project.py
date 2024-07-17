import logging

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, OuterRef, Subquery
from django.forms import Form
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import DeleteView, DetailView, TemplateView
from django.views.generic.edit import FormMixin

from rdmo.core.plugins import get_plugin, get_plugins
from rdmo.core.views import CSRFViewMixin, ObjectPermissionMixin, RedirectViewMixin, StoreIdViewMixin
from rdmo.questions.models import Catalog
from rdmo.questions.utils import get_widgets
from rdmo.tasks.models import Task
from rdmo.views.models import View

from ..models import Integration, Invite, Membership, Project
from ..utils import get_upload_accept

logger = logging.getLogger(__name__)


class ProjectsView(LoginRequiredMixin, CSRFViewMixin, StoreIdViewMixin, TemplateView):
    template_name = 'projects/projects.html'


class ProjectDetailView(ObjectPermissionMixin, DetailView):
    model = Project
    queryset = Project.objects.prefetch_related(
        'issues',
        'issues__task',
        'issues__task__conditions',
        'issues__task__conditions__source',
        'issues__task__conditions__target_option',
        'tasks',
        'views',
        'values'
    )
    permission_required = 'projects.view_project_object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = context['project']
        ancestors = project.get_ancestors(include_self=True)
        values = project.values.filter(snapshot=None).select_related('attribute', 'option')
        highest = Membership.objects.filter(project__in=ancestors, user_id=OuterRef('user_id')) \
                                    .order_by('-project__level')
        memberships = Membership.objects.filter(project__in=ancestors) \
                                        .annotate(highest=Subquery(highest.values('project__level')[:1])) \
                                        .filter(highest=F('project__level')) \
                                        .select_related('user')

        if settings.SOCIALACCOUNT:
            # prefetch the users social account, if that relation exists
            memberships = memberships.prefetch_related('user__socialaccount_set')

        integrations = Integration.objects.filter(project__in=ancestors)
        context['catalogs'] = Catalog.objects.filter_current_site() \
                                             .filter_group(self.request.user) \
                                             .filter_availability(self.request.user)
        context['tasks_available'] = Task.objects.filter_current_site() \
                                                 .filter_catalog(self.object.catalog) \
                                                 .filter_group(self.request.user) \
                                                 .filter_availability(self.request.user).exists()
        context['views_available'] = View.objects.filter_current_site() \
                                                 .filter_catalog(self.object.catalog) \
                                                 .filter_group(self.request.user) \
                                                 .filter_availability(self.request.user).exists()
        ancestors_import = []
        for instance in ancestors.exclude(id=project.id):
            if self.request.user.has_perm('projects.view_project_object', instance):
                ancestors_import.append(instance)
        context['ancestors_import'] = ancestors_import
        context['memberships'] = memberships.order_by('user__last_name', '-project__level')
        context['integrations'] = integrations.order_by('provider_key', '-project__level')
        context['providers'] = get_plugins('PROJECT_ISSUE_PROVIDERS')
        context['issues'] = [
            issue for issue in project.issues.order_by('-status', 'task__order', 'task__uri') if issue.resolve(values)
        ]
        context['views'] = project.views.order_by('order', 'uri')
        context['snapshots'] = project.snapshots.all()
        context['invites'] = project.invites.all()
        context['membership'] = Membership.objects.filter(project=project, user=self.request.user).first()
        context['upload_accept'] = get_upload_accept()
        return context


class ProjectDeleteView(ObjectPermissionMixin, RedirectViewMixin, DeleteView):
    model = Project
    queryset = Project.objects.all()
    success_url = reverse_lazy('projects')
    permission_required = 'projects.delete_project_object'


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


class ProjectCancelView(LoginRequiredMixin, RedirectViewMixin, TemplateView):
    template_name = 'core/error.html'
    success_url = reverse_lazy('projects')

    def get(self, request, token=None):
        invite = get_object_or_404(Invite, token=token)
        if invite.user in [None, request.user]:
            invite.delete()

        return redirect(self.success_url)


class ProjectLeaveView(ObjectPermissionMixin, RedirectViewMixin, FormMixin, DetailView):
    model = Project
    form_class = Form
    queryset = Project.objects.all()
    success_url = reverse_lazy('projects')
    permission_required = 'projects.leave_project_object'
    template_name = 'projects/project_confirm_leave.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid() and 'cancel' not in request.POST:
            membership = Membership.objects.filter(project=self.get_object()).get(user=request.user)
            if not membership.is_last_owner:
                membership.delete()

        return redirect(self.success_url)


class ProjectExportView(ObjectPermissionMixin, DetailView):
    model = Project
    queryset = Project.objects.all()
    permission_required = 'projects.export_project_object'

    def get_export_plugin(self):
        export_plugin = get_plugin('PROJECT_EXPORTS', self.kwargs.get('format'))
        if export_plugin is None:
            raise Http404

        export_plugin.request = self.request
        export_plugin.project = self.object

        return export_plugin

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.get_export_plugin().render()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.get_export_plugin().submit()


class ProjectQuestionsView(ObjectPermissionMixin, DetailView):
    model = Project
    queryset = Project.objects.all()
    permission_required = 'projects.view_project_object'
    template_name = 'projects/project_questions.html'

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.catalog is None:
            return redirect('project_error', pk=self.object.pk)
        else:
            context = self.get_context_data(object=self.object)
            context['widgets'] = {widget.template_name for widget in get_widgets() if widget.template_name}
            return self.render_to_response(context)


class ProjectErrorView(ObjectPermissionMixin, DetailView):
    model = Project
    queryset = Project.objects.all()
    permission_required = 'projects.view_project_object'
    template_name = 'projects/project_error.html'
