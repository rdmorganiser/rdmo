import logging

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import models
from django.http import (Http404, HttpResponseBadRequest,
                         HttpResponseForbidden, HttpResponseRedirect)
from django.shortcuts import get_object_or_404, redirect, render
from django.template import TemplateSyntaxError
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import (CreateView, DeleteView, DetailView,
                                  TemplateView, UpdateView)
from django.views.generic.base import View as BaseView
from django_filters.views import FilterView
from rdmo.accounts.utils import is_site_manager
from rdmo.core.imports import handle_uploaded_file
from rdmo.core.utils import import_class, render_to_format
from rdmo.core.views import ObjectPermissionMixin, RedirectViewMixin
from rdmo.questions.models import Catalog
from rdmo.tasks.models import Task
from rdmo.views.models import View

from .filters import ProjectFilter
from .forms import (MembershipCreateForm, ProjectForm, ProjectTasksForm,
                    ProjectViewsForm, SnapshotCreateForm)
from .models import Membership, Project, Snapshot
from .utils import (get_answers_tree, is_last_owner,
                    save_import_snapshot_values, save_import_tasks,
                    save_import_values, save_import_views)

log = logging.getLogger(__name__)


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

        return Project.objects.filter(user=self.request.user).annotate(role=models.Case(
            *case_args,
            default=None,
            output_field=models.CharField()
        ))

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
            return Project.objects.filter_current_site()
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

        context['tasks'] = project.tasks.active(project)
        context['snapshots'] = project.snapshots.all()
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


class ProjectCreateUploadView(LoginRequiredMixin, BaseView):
    success_url = reverse_lazy('projects')

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.success_url)

    def post(self, request, *args, **kwargs):
        try:
            uploaded_file = request.FILES['uploaded_file']
        except KeyError:
            return HttpResponseRedirect(self.success_url)
        else:
            import_tmpfile_name = handle_uploaded_file(uploaded_file)

        for key, title, import_class_name in settings.PROJECT_IMPORTS:
            project_import = import_class(import_class_name)(import_tmpfile_name)

            if project_import.check():
                try:
                    project_import.process()
                except ValidationError as e:
                    return render(request, 'core/error.html', {
                        'title': _('Import error'),
                        'errors': e
                    }, status=400)

                # store information in session for ProjectCreateImportView
                request.session['create_import_tmpfile_name'] = import_tmpfile_name
                request.session['create_import_class_name'] = import_class_name

                return render(request, 'projects/project_upload.html', {
                    'create': True,
                    'file_name': uploaded_file.name,
                    'project': project_import.project,
                    'values': project_import.values,
                    'snapshots': project_import.snapshots,
                    'tasks': project_import.tasks,
                    'views': project_import.views
                })

        return render(request, 'core/error.html', {
            'title': _('Import error'),
            'errors': [_('Files of this type cannot be imported.')]
        }, status=400)


class ProjectCreateImportView(LoginRequiredMixin, TemplateView):
    success_url = reverse_lazy('projects')

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.success_url)

    def post(self, request, *args, **kwargs):
        import_tmpfile_name = request.session.get('create_import_tmpfile_name')
        import_class_name = request.session.get('create_import_class_name')
        checked = [key for key, value in request.POST.items() if 'on' in value]

        if import_tmpfile_name and import_class_name:
            project_import = import_class(import_class_name)(import_tmpfile_name)

            if project_import.check():
                try:
                    project_import.process()
                except ValidationError as e:
                    return render(request, 'core/error.html', {
                        'title': _('Import error'),
                        'errors': e
                    }, status=400)

                # add current site and save project
                project_import.project.site = get_current_site(self.request)
                project_import.project.save()

                # add user to project
                membership = Membership(project=project_import.project, user=request.user, role='owner')
                membership.save()

                save_import_values(project_import.project, project_import.values, checked)
                save_import_snapshot_values(project_import.project, project_import.snapshots, checked)
                save_import_tasks(project_import.project, project_import.tasks)
                save_import_views(project_import.project, project_import.views)

                return HttpResponseRedirect(project_import.project.get_absolute_url())

        return render(request, 'core/error.html', {
            'title': _('Import error'),
            'errors': [_('There has been an error with your import.')]
        }, status=400)


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


class ProjectExportView(ObjectPermissionMixin, DetailView):
    model = Project
    queryset = Project.objects.all()
    permission_required = 'projects.export_project_object'

    def render_to_response(self, context, **response_kwargs):
        # search for the format in the settings.PROJECT_EXPORTS list
        try:
            key, title, export_class_name = next(item for item in settings.PROJECT_EXPORTS if item[0] == self.kwargs['format'])
        except (KeyError, StopIteration):
            # format not given or not found
            raise Http404

        export_class = import_class(export_class_name)
        export = export_class(context['project'])

        return export.render()


class ProjectUpdateUploadView(ObjectPermissionMixin, RedirectViewMixin, UpdateView):
    model = Project
    queryset = Project.objects.all()
    form_class = ProjectTasksForm
    permission_required = 'projects.import_project_object'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        current_project = self.object

        try:
            uploaded_file = request.FILES['uploaded_file']
        except KeyError:
            return HttpResponseRedirect(self.get_success_url())
        else:
            import_tmpfile_name = handle_uploaded_file(uploaded_file)

        for key, title, import_class_name in settings.PROJECT_IMPORTS:
            project_import = import_class(import_class_name)(import_tmpfile_name, current_project)

            if project_import.check():
                try:
                    project_import.process()
                except ValidationError as e:
                    return render(request, 'core/error.html', {
                        'title': _('Import error'),
                        'errors': e
                    }, status=400)

                # store information in session for ProjectCreateImportView
                request.session['update_import_tmpfile_name'] = import_tmpfile_name
                request.session['update_import_class_name'] = import_class_name

                return render(request, 'projects/project_upload.html', {
                    'file_name': uploaded_file.name,
                    'current_project': current_project,
                    'values': project_import.values,
                    'tasks': project_import.tasks,
                    'views': project_import.views
                })

        return render(request, 'core/error.html', {
            'title': _('Import error'),
            'errors': [_('Files of this type cannot be imported.')]
        }, status=400)


class ProjectUpdateImportView(ObjectPermissionMixin, UpdateView):
    model = Project
    queryset = Project.objects.all()
    form_class = ProjectTasksForm
    permission_required = 'projects.import_project_object'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        current_project = self.object

        import_tmpfile_name = request.session.get('update_import_tmpfile_name')
        import_class_name = request.session.get('update_import_class_name')
        checked = [key for key, value in request.POST.items() if 'on' in value]

        if import_tmpfile_name and import_class_name:
            project_import = import_class(import_class_name)(import_tmpfile_name, current_project)

            if project_import.check():
                try:
                    project_import.process()
                except ValidationError as e:
                    return render(request, 'core/error.html', {
                        'title': _('Import error'),
                        'errors': e
                    }, status=400)

                save_import_values(current_project, project_import.values, checked)
                save_import_tasks(current_project, project_import.tasks)
                save_import_views(current_project, project_import.views)

                return HttpResponseRedirect(current_project.get_absolute_url())

        return render(request, 'core/error.html', {
            'title': _('Import error'),
            'errors': [_('There has been an error with your import.')]
        }, status=400)


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
