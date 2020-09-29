import logging

from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.generic import UpdateView

from rdmo.core.imports import handle_uploaded_file
from rdmo.core.plugins import get_plugin, get_plugins
from rdmo.core.utils import import_class
from rdmo.core.views import ObjectPermissionMixin, RedirectViewMixin
from rdmo.questions.models import Catalog
from rdmo.tasks.models import Task
from rdmo.views.models import View

from ..forms import ProjectForm, ProjectTasksForm, ProjectViewsForm
from ..models import Project
from ..utils import save_import_tasks, save_import_values, save_import_views

logger = logging.getLogger(__name__)


class ProjectUpdateView(ObjectPermissionMixin, RedirectViewMixin, UpdateView):
    model = Project
    queryset = Project.objects.all()
    form_class = ProjectForm
    permission_required = 'projects.change_project_object'

    def get_form_kwargs(self):
        catalogs = Catalog.objects.filter_current_site() \
                                  .filter_group(self.request.user) \
                                  .filter_availability(self.request.user)

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
        tasks = Task.objects.filter_current_site() \
                            .filter_group(self.request.user) \
                            .filter_availability(self.request.user)

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
        views = View.objects.filter_current_site() \
                            .filter_catalog(self.object.catalog) \
                            .filter_group(self.request.user) \
                            .filter_availability(self.request.user)

        form_kwargs = super().get_form_kwargs()
        form_kwargs.update({
            'views': views
        })
        return form_kwargs


class ProjectUpdateUploadView(ObjectPermissionMixin, RedirectViewMixin, UpdateView):
    model = Project
    queryset = Project.objects.all()
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

        for import_key, import_plugin in get_plugins('PROJECT_IMPORTS').items():
            import_plugin.file_name = import_tmpfile_name
            import_plugin.current_project = current_project

            if import_plugin.check():
                try:
                    import_plugin.process()
                except ValidationError as e:
                    return render(request, 'core/error.html', {
                        'title': _('Import error'),
                        'errors': e
                    }, status=400)

                # store information in session for ProjectCreateImportView
                request.session['update_import_tmpfile_name'] = import_tmpfile_name
                request.session['update_import_key'] = import_key

                return render(request, 'projects/project_upload.html', {
                    'file_name': uploaded_file.name,
                    'current_project': current_project,
                    'values': import_plugin.values,
                    'tasks': import_plugin.tasks,
                    'views': import_plugin.views
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
        import_key = request.session.get('update_import_key')
        checked = [key for key, value in request.POST.items() if 'on' in value]

        if import_tmpfile_name and import_key:
            import_plugin = get_plugin('PROJECT_IMPORTS', import_key)
            import_plugin.file_name = import_tmpfile_name
            import_plugin.current_project = current_project

            if import_plugin.check():
                try:
                    import_plugin.process()
                except ValidationError as e:
                    return render(request, 'core/error.html', {
                        'title': _('Import error'),
                        'errors': e
                    }, status=400)

                save_import_values(current_project, import_plugin.values, checked)
                save_import_tasks(current_project, import_plugin.tasks)
                save_import_views(current_project, import_plugin.views)

                return HttpResponseRedirect(current_project.get_absolute_url())

        return render(request, 'core/error.html', {
            'title': _('Import error'),
            'errors': [_('There has been an error with your import.')]
        }, status=400)
