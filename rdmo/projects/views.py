from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import models
from django.http import HttpResponse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.template import TemplateSyntaxError
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from rdmo.core.views import ObjectPermissionMixin, RedirectViewMixin
from rdmo.core.utils import render_to_format
from rdmo.tasks.models import Task
from rdmo.views.models import View

from .models import Project, Membership, Snapshot
from .forms import ProjectForm, SnapshotCreateForm, MembershipCreateForm
from .serializers.export import ProjectSerializer as ExportSerializer
from .renderers import XMLRenderer
from .utils import get_answers_tree


class ProjectsView(LoginRequiredMixin, ListView):
    template_name = 'projects/projects.html'
    context_object_name = 'projects'

    def get_queryset(self):
        # prepare When statements for conditional expression
        case_args = []
        for role, text in Membership.ROLE_CHOICES:
            case_args.append(models.When(membership__role=role, then=models.Value(str(text))))

        return Project.objects.filter(user=self.request.user).annotate(role=models.Case(
            *case_args,
            default=None,
            output_field=models.CharField()
        ))


class ProjectDetailView(ObjectPermissionMixin, DetailView):
    model = Project
    permission_required = 'projects.view_project_object'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)

        context['memberships'] = []
        for membership in Membership.objects.filter(project=context['project']).order_by('user__last_name'):
            context['memberships'].append({
                'id': membership.id,
                'user': membership.user,
                'role': dict(Membership.ROLE_CHOICES)[membership.role]
            })

        context['tasks'] = Task.objects.active_by_project(context['project'])
        context['views'] = View.objects.all()
        context['snapshots'] = context['project'].snapshots.all()
        return context


class ProjectCreateView(LoginRequiredMixin, RedirectViewMixin, CreateView):
    model = Project
    form_class = ProjectForm

    def form_valid(self, form):
        response = super(ProjectCreateView, self).form_valid(form)

        # add current user as owner
        membership = Membership(project=form.instance, user=self.request.user, role='owner')
        membership.save()

        return response


class ProjectUpdateView(ObjectPermissionMixin, RedirectViewMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    permission_required = 'projects.change_project_object'


class ProjectDeleteView(ObjectPermissionMixin, RedirectViewMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('projects')
    permission_required = 'projects.delete_project_object'


class ProjectExportXMLView(ObjectPermissionMixin, DetailView):
    model = Project
    permission_required = 'projects.export_project_object'

    def render_to_response(self, context, **response_kwargs):
        serializer = ExportSerializer(context['project'])
        response = HttpResponse(XMLRenderer().render(serializer.data), content_type="application/xml")
        response['Content-Disposition'] = 'filename="%s.xml"' % context['project'].title
        return response


class SnapshotCreateView(ObjectPermissionMixin, RedirectViewMixin, CreateView):
    model = Snapshot
    form_class = SnapshotCreateForm
    permission_required = 'projects.add_snapshot_object'

    def dispatch(self, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return super(SnapshotCreateView, self).dispatch(*args, **kwargs)

    def get_permission_object(self):
        return self.project

    def get_form_kwargs(self):
        kwargs = super(SnapshotCreateView, self).get_form_kwargs()
        kwargs['project'] = self.project
        return kwargs


class SnapshotUpdateView(ObjectPermissionMixin, RedirectViewMixin, UpdateView):
    model = Snapshot
    fields = ['title', 'description']
    permission_required = 'projects.change_snapshot_object'

    def get_permission_object(self):
        return self.get_object().project


class SnapshotRollbackView(ObjectPermissionMixin, RedirectViewMixin, DetailView):
    model = Snapshot
    permission_required = 'projects.rollback_snapshot_object'
    template_name = 'projects/snapshot_rollback.html'

    def get_permission_object(self):
        return self.get_object().project

    def post(self, request, *args, **kwargs):
        snapshot = self.get_object()

        if 'cancel' not in request.POST:
            snapshot.rollback()

        return HttpResponseRedirect(reverse('project', args=[snapshot.project.id]))


class MembershipCreateView(ObjectPermissionMixin, RedirectViewMixin, CreateView):
    model = Membership
    form_class = MembershipCreateForm
    permission_required = 'projects.add_membership_object'

    def dispatch(self, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return super(MembershipCreateView, self).dispatch(*args, **kwargs)

    def get_permission_object(self):
        return self.project

    def get_form_kwargs(self):
        kwargs = super(MembershipCreateView, self).get_form_kwargs()
        kwargs['project'] = self.project
        return kwargs


class MembershipUpdateView(ObjectPermissionMixin, RedirectViewMixin, UpdateView):
    model = Membership
    fields = ('role', )
    permission_required = 'projects.change_membership_object'

    def get_permission_object(self):
        return self.get_object().project


class MembershipDeleteView(ObjectPermissionMixin, RedirectViewMixin, DeleteView):
    model = Membership
    permission_required = 'projects.delete_membership_object'

    def get_permission_object(self):
        return self.get_object().project

    def get_success_url(self):
        return reverse('project', args=[self.get_object().project.id])


class ProjectAnswersView(ObjectPermissionMixin, DetailView):
    model = Project
    permission_required = 'projects.view_project_object'
    template_name = 'projects/project_answers.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectAnswersView, self).get_context_data(**kwargs)

        try:
            current_snapshot = context['project'].snapshots.get(pk=self.kwargs.get('snapshot_id'))
        except Snapshot.DoesNotExist:
            current_snapshot = None

        context.update({
            'current_snapshot': current_snapshot,
            'snapshots': list(context['project'].snapshots.values('id', 'title')),
            'answers_tree': get_answers_tree(context['project'], current_snapshot),
            'export_formats': settings.EXPORT_FORMATS
        })

        return context


class ProjectAnswersExportView(ObjectPermissionMixin, DetailView):
    model = Project
    permission_required = 'projects.view_project_object'

    def get_context_data(self, **kwargs):
        context = super(ProjectAnswersExportView, self).get_context_data(**kwargs)

        try:
            current_snapshot = context['project'].snapshots.get(pk=self.kwargs.get('snapshot_id'))
        except Snapshot.DoesNotExist:
            current_snapshot = None

        context.update({
            'format': self.kwargs.get('format'),
            'title': context['project'].title,
            'answers_tree': get_answers_tree(context['project'], current_snapshot)
        })
        return context

    def render_to_response(self, context, **response_kwargs):
        return render_to_format(self.request, context['format'], context['title'], 'projects/project_answers_export.html', context)


class ProjectViewView(ObjectPermissionMixin, DetailView):
    model = Project
    permission_required = 'projects.view_project_object'
    template_name = 'projects/project_view.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectViewView, self).get_context_data(**kwargs)

        try:
            context['current_snapshot'] = context['project'].snapshots.get(pk=self.kwargs.get('snapshot_id'))
        except Snapshot.DoesNotExist:
            context['current_snapshot'] = None

        try:
            context['view'] = View.objects.get(pk=self.kwargs.get('view_id'))
        except View.DoesNotExist:
            raise Http404

        try:
            context['rendered_view'] = context['view'].render(context['project'], context['current_snapshot'])
        except TemplateSyntaxError:
            context['rendered_view'] = None

        context.update({
            'snapshots': list(context['project'].snapshots.values('id', 'title')),
            'export_formats': settings.EXPORT_FORMATS
        })

        return context


class ProjectViewExportView(ObjectPermissionMixin, DetailView):
    model = Project
    permission_required = 'projects.view_project_object'

    def get_context_data(self, **kwargs):
        context = super(ProjectViewExportView, self).get_context_data(**kwargs)

        try:
            context['current_snapshot'] = context['project'].snapshots.get(pk=self.kwargs.get('snapshot_id'))
        except Snapshot.DoesNotExist:
            context['current_snapshot'] = None

        try:
            context['view'] = View.objects.get(pk=self.kwargs.get('view_id'))
        except View.DoesNotExist:
            raise Http404

        try:
            context['rendered_view'] = context['view'].render(context['project'], context['current_snapshot'])
        except TemplateSyntaxError:
            context['rendered_view'] = None

        context.update({
            'format': self.kwargs.get('format'),
            'title': context['project'].title
        })

        return context

    def render_to_response(self, context, **response_kwargs):
        return render_to_format(self.request, context['format'], context['title'], 'projects/project_view_export.html', context)


class ProjectQuestionsView(ObjectPermissionMixin, DetailView):
    model = Project
    permission_required = 'projects.view_project_object'
    template_name = 'projects/project_questions.html'
