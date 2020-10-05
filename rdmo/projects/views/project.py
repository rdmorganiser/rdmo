import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import models
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import DeleteView, DetailView
from django_filters.views import FilterView

from rdmo.accounts.utils import is_site_manager
from rdmo.core.plugins import get_plugin, get_plugins
from rdmo.core.views import ObjectPermissionMixin, RedirectViewMixin

from ..filters import ProjectFilter
from ..models import Membership, Project, Value
from ..utils import is_last_owner

logger = logging.getLogger(__name__)


class ProjectsView(LoginRequiredMixin, FilterView):
    template_name = 'projects/projects.html'
    context_object_name = 'projects'
    paginate_by = 20
    filterset_class = ProjectFilter

    def get_queryset(self):
        # prepare When statements for conditional expression
        case_args = []
        for role, text in Membership.ROLE_CHOICES:
            case_args.append(models.When(membership__role=role, then=models.Value(str(text))))

        # prepare subquery for last_changed
        subquery = Value.objects.filter(project=models.OuterRef('pk')).order_by('-updated').values('updated')[:1]

        return Project.objects.filter(user=self.request.user) \
                              .annotate(role=models.Case(*case_args, default=None, output_field=models.CharField()),
                                        last_changed=models.functions.Greatest('updated', models.Subquery(subquery)))

    def get_context_data(self, **kwargs):
        context = super(ProjectsView, self).get_context_data(**kwargs)
        context['is_site_manager'] = is_site_manager(self.request.user)
        return context


class SiteProjectsView(LoginRequiredMixin, FilterView):
    template_name = 'projects/site_projects.html'
    context_object_name = 'projects'
    paginate_by = 20
    filterset_class = ProjectFilter
    model = Project

    def get_queryset(self):
        if is_site_manager(self.request.user):

            # prepare subquery for last_changed
            subquery = Value.objects.filter(project=models.OuterRef('pk')).order_by('-updated').values('updated')[:1]

            return Project.objects.filter_current_site() \
                                  .annotate(last_changed=models.functions.Greatest('updated', models.Subquery(subquery)))
        else:
            raise PermissionDenied()


class ProjectDetailView(ObjectPermissionMixin, DetailView):
    model = Project
    queryset = Project.objects.all()
    permission_required = 'projects.view_project_object'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        project = context['project']

        context['memberships'] = []
        for membership in Membership.objects.filter(project=project).order_by('user__last_name'):
            context['memberships'].append({
                'id': membership.id,
                'user': membership.user,
                'role': dict(Membership.ROLE_CHOICES)[membership.role],
                'last_owner': is_last_owner(project, membership.user),
            })

        context['providers'] = get_plugins('SERVICE_PROVIDERS')
        context['integrations'] = project.integrations.all()
        context['issues'] = project.issues.active()
        context['snapshots'] = project.snapshots.all()
        return context


class ProjectDeleteView(ObjectPermissionMixin, RedirectViewMixin, DeleteView):
    model = Project
    queryset = Project.objects.all()
    success_url = reverse_lazy('projects')
    permission_required = 'projects.delete_project_object'


class ProjectExportView(ObjectPermissionMixin, DetailView):
    model = Project
    queryset = Project.objects.all()
    permission_required = 'projects.export_project_object'

    def render_to_response(self, context, **response_kwargs):
        export_plugin = get_plugin('PROJECT_EXPORTS', self.kwargs.get('format'))
        if export_plugin is None:
            raise Http404

        export_plugin.project = context['project']
        export_plugin.snapshot = None

        return export_plugin.render()


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
            return self.render_to_response(context)


class ProjectErrorView(ObjectPermissionMixin, DetailView):
    model = Project
    queryset = Project.objects.all()
    permission_required = 'projects.view_project_object'
    template_name = 'projects/project_error.html'
