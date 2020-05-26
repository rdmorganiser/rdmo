import logging
import re

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.db import models
from django.http import (Http404, HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden, HttpResponseRedirect)
from django.shortcuts import get_object_or_404, redirect, render
from django.template import TemplateSyntaxError
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import (CreateView, DeleteView, DetailView,
                                  TemplateView, UpdateView)
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.base import View as BaseView

from rdmo.accounts.utils import is_site_manager
from rdmo.core.exports import prettify_xml
from rdmo.core.imports import handle_uploaded_file, read_xml_file
from rdmo.core.utils import render_to_csv, render_to_format
from rdmo.core.views import ObjectPermissionMixin, RedirectViewMixin
from rdmo.projects.imports import import_project
from rdmo.questions.models import Catalog
from rdmo.tasks.models import Task
from rdmo.views.models import View

from .forms import (MembershipCreateForm, ProjectForm, ProjectTasksForm,
                    ProjectViewsForm, SnapshotCreateForm)
from .models import Membership, Project, Snapshot
from .renderers import XMLRenderer
from .serializers.export import ProjectSerializer as ExportSerializer
from .utils import get_answers_tree, is_last_owner

log = logging.getLogger(__name__)


class ProjectsView(LoginRequiredMixin, TemplateResponseMixin, BaseView):
    template_name = 'projects/projects.html'
    context_object_name = 'projects'

    def get(self, request):
        site_manager = is_site_manager(request.user)

        return self.render_to_response({
            'site_manager': site_manager,
            'user_projects': self.get_user_projects(),
            'site_projects': self.get_site_projects(site_manager),
        })

    def get_user_projects(self):
        # prepare When statements for conditional expression
        case_args = []
        for role, text in Membership.ROLE_CHOICES:
            case_args.append(models.When(membership__role=role, then=models.Value(str(text))))

        return Project.objects.filter(user=self.request.user).annotate(role=models.Case(
            *case_args,
            default=None,
            output_field=models.CharField()
        ))

    def get_site_projects(self, site_manager):
        if site_manager:
            return Project.objects.filter_current_site()
        else:
            return []


class ProjectDetailView(ObjectPermissionMixin, DetailView):
    model = Project
    queryset = Project.objects.all()
    permission_required = 'projects.view_project_object'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)

        context['memberships'] = []
        for membership in Membership.objects.filter(project=context['project']).order_by('user__last_name'):
            context['memberships'].append({
                'id': membership.id,
                'user': membership.user,
                'role': dict(Membership.ROLE_CHOICES)[membership.role],
                'last_owner': is_last_owner(context['project'], membership.user),
            })

        context['snapshots'] = context['project'].snapshots.all()
        return context


class ProjectCreateView(LoginRequiredMixin, RedirectViewMixin, CreateView):
    model = Project
    form_class = ProjectForm

    def get_form_kwargs(self):
        catalogs = Catalog.objects.filter_current_site().filter_group(self.request.user)

        form_kwargs = super().get_form_kwargs()
        form_kwargs.update({
            'catalogs': catalogs
        })
        return form_kwargs

    def form_valid(self, form):
        # add current site
        form.instance.site = get_current_site(self.request)

        # save the project
        response = super(ProjectCreateView, self).form_valid(form)

        # add all tasks to project
        tasks = Task.objects.filter_current_site().filter_group(self.request.user)
        for task in tasks:
            form.instance.tasks.add(task)

        # add all views to project
        views = View.objects.filter_current_site().filter_catalog(self.object.catalog).filter_group(self.request.user)
        for view in views:
            form.instance.views.add(view)

        # add current user as owner
        membership = Membership(project=form.instance, user=self.request.user, role='owner')
        membership.save()

        return response


class ProjectUpdateView(ObjectPermissionMixin, RedirectViewMixin, UpdateView):
    model = Project
    queryset = Project.objects.all()
    form_class = ProjectForm
    permission_required = 'projects.change_project_object'

    def get_form_kwargs(self):
        catalogs = Catalog.objects.filter_current_site().filter_group(self.request.user)

        form_kwargs = super().get_form_kwargs()
        form_kwargs.update({
            'catalogs': catalogs
        })
        return form_kwargs


class ProjectUpdateTasksView(ObjectPermissionMixin, RedirectViewMixin, UpdateView):
    model = Project
    queryset = Project.objects.all()
    form_class = ProjectTasksForm
    permission_required = 'projects.change_project_object'

    def get_form_kwargs(self):
        tasks = Task.objects.filter_current_site().filter_group(self.request.user)

        form_kwargs = super().get_form_kwargs()
        form_kwargs.update({
            'tasks': tasks
        })
        return form_kwargs


class ProjectUpdateViewsView(ObjectPermissionMixin, RedirectViewMixin, UpdateView):
    model = Project
    queryset = Project.objects.all()
    form_class = ProjectViewsForm
    permission_required = 'projects.change_project_object'

    def get_form_kwargs(self):
        views = View.objects.filter_current_site().filter_catalog(self.object.catalog).filter_group(self.request.user)

        form_kwargs = super().get_form_kwargs()
        form_kwargs.update({
            'views': views
        })
        return form_kwargs


class ProjectDeleteView(ObjectPermissionMixin, RedirectViewMixin, DeleteView):
    model = Project
    queryset = Project.objects.all()
    success_url = reverse_lazy('projects')
    permission_required = 'projects.delete_project_object'


class ProjectExportXMLView(ObjectPermissionMixin, DetailView):
    model = Project
    queryset = Project.objects.all()
    permission_required = 'projects.export_project_object'

    def render_to_response(self, context, **response_kwargs):
        serializer = ExportSerializer(context['project'])
        xmldata = XMLRenderer().render(serializer.data)
        response = HttpResponse(prettify_xml(xmldata), content_type="application/xml")
        response['Content-Disposition'] = 'filename="%s.xml"' % context['project'].title
        return response


class ProjectExportCSVView(ObjectPermissionMixin, DetailView):
    model = Project
    queryset = Project.objects.all()
    permission_required = 'projects.export_project_object'

    def stringify_answers(self, answers):
        if answers is not None:
            return '; '.join([self.stringify(answer) for answer in answers])
        else:
            return ''

    def stringify(self, el):
        if el is None:
            return ''
        else:
            return re.sub(r'\s+', ' ', str(el))

    def render_to_response(self, context, **response_kwargs):

        if self.kwargs.get('format') == 'csvsemicolon':
            delimiter = ';'
        else:
            delimiter = ','

        data = []
        answer_sections = get_answers_tree(context['project']).get('sections')
        for section in answer_sections:
            questionsets = section.get('questionsets')
            for questionset in questionsets:
                questions = questionset.get('questions')
                for question in questions:
                    text = self.stringify(question.get('text'))
                    answers = self.stringify_answers(question.get('answers'))
                    data.append((text, answers))

        return render_to_csv(context['project'].title, data, delimiter)


class ProjectImportXMLView(LoginRequiredMixin, TemplateView):
    success_url = reverse_lazy('projects')
    parsing_error_template = 'core/import_parsing_error.html'

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.success_url)

    def post(self, request, *args, **kwargs):
        try:
            request.FILES['uploaded_file']
        except KeyError:
            return HttpResponseRedirect(self.success_url)
        else:
            tempfilename = handle_uploaded_file(request.FILES['uploaded_file'])

        tree = read_xml_file(tempfilename)
        if tree is None:
            log.info('Xml parsing error. Import failed.')
            return render(request, self.parsing_error_template, status=400)
        else:
            import_project(request.user, tree)
            return HttpResponseRedirect(self.success_url)


class SnapshotCreateView(ObjectPermissionMixin, RedirectViewMixin, CreateView):
    model = Snapshot
    form_class = SnapshotCreateForm
    permission_required = 'projects.add_snapshot_object'

    def dispatch(self, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.all(), pk=self.kwargs['project_id'])
        return super(SnapshotCreateView, self).dispatch(*args, **kwargs)

    def get_permission_object(self):
        return self.project

    def get_form_kwargs(self):
        kwargs = super(SnapshotCreateView, self).get_form_kwargs()
        kwargs['project'] = self.project
        return kwargs


class SnapshotUpdateView(ObjectPermissionMixin, RedirectViewMixin, UpdateView):
    model = Snapshot
    queryset = Snapshot.objects.all()
    fields = ['title', 'description']
    permission_required = 'projects.change_snapshot_object'

    def get_permission_object(self):
        return self.get_object().project


class SnapshotRollbackView(ObjectPermissionMixin, RedirectViewMixin, DetailView):
    model = Snapshot
    queryset = Snapshot.objects.all()
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
        self.project = get_object_or_404(Project.objects.all(), pk=self.kwargs['project_id'])
        return super(MembershipCreateView, self).dispatch(*args, **kwargs)

    def get_permission_object(self):
        return self.project

    def get_form_kwargs(self):
        kwargs = super(MembershipCreateView, self).get_form_kwargs()
        kwargs['project'] = self.project
        return kwargs


class MembershipUpdateView(ObjectPermissionMixin, RedirectViewMixin, UpdateView):
    model = Membership
    queryset = Membership.objects.all()
    fields = ('role', )
    permission_required = 'projects.change_membership_object'

    def get_permission_object(self):
        return self.get_object().project


class MembershipDeleteView(ObjectPermissionMixin, RedirectViewMixin, DeleteView):
    model = Membership
    queryset = Membership.objects.all()
    permission_required = 'projects.delete_membership_object'

    def delete(self, *args, **kwargs):
        self.obj = self.get_object()

        if (self.request.user in self.obj.project.owners) or is_site_manager(self.request.user):
            # user is owner or site manager
            if is_last_owner(self.obj.project, self.obj.user):
                log.info('User "%s" not allowed to remove last user "%s"', self.request.user.username, self.obj.user.username)
                return HttpResponseBadRequest()
            else:
                log.info('User "%s" deletes user "%s"', self.request.user.username, self.obj.user.username)
                success_url = reverse('project', args=[self.get_object().project.id])
                self.obj.delete()
                return HttpResponseRedirect(success_url)

        elif self.request.user == self.obj.user:
            # user wants to remove him/herself
            log.info('User "%s" deletes himself.', self.request.user.username)
            success_url = reverse('projects')
            self.obj.delete()
            return HttpResponseRedirect(success_url)

        else:
            log.info('User "%s" not allowed to remove user "%s"', self.request.user.username, self.obj.user.username)
            return HttpResponseForbidden()

    def get_permission_object(self):
        return self.get_object().project


class ProjectAnswersView(ObjectPermissionMixin, DetailView):
    model = Project
    queryset = Project.objects.all()
    permission_required = 'projects.view_project_object'
    template_name = 'projects/project_answers.html'
    no_catalog_error_template = 'projects/project_error_no_catalog.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.catalog is None:
            return redirect('project_error', pk=self.object.pk)
        else:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)

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
    queryset = Project.objects.all()
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
    queryset = Project.objects.all()
    permission_required = 'projects.view_project_object'
    template_name = 'projects/project_view.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectViewView, self).get_context_data(**kwargs)

        try:
            context['current_snapshot'] = context['project'].snapshots.get(pk=self.kwargs.get('snapshot_id'))
        except Snapshot.DoesNotExist:
            context['current_snapshot'] = None

        try:
            context['view'] = context['project'].views.get(pk=self.kwargs.get('view_id'))
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
    queryset = Project.objects.all()
    permission_required = 'projects.view_project_object'

    def get_context_data(self, **kwargs):
        context = super(ProjectViewExportView, self).get_context_data(**kwargs)

        try:
            context['current_snapshot'] = context['project'].snapshots.get(pk=self.kwargs.get('snapshot_id'))
        except Snapshot.DoesNotExist:
            context['current_snapshot'] = None

        try:
            context['view'] = context['project'].views.get(pk=self.kwargs.get('view_id'))
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
