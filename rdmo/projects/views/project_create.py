import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, TemplateView
from django.views.generic.base import View as BaseView

from rdmo.core.imports import handle_uploaded_file
from rdmo.core.plugins import get_plugin, get_plugins
from rdmo.core.views import RedirectViewMixin
from rdmo.questions.models import Catalog
from rdmo.tasks.models import Task
from rdmo.views.models import View

from ..forms import ProjectForm
from ..models import Membership, Project
from ..utils import (save_import_snapshot_values, save_import_tasks,
                     save_import_values, save_import_views)

logger = logging.getLogger(__name__)


class ProjectCreateView(LoginRequiredMixin, RedirectViewMixin, CreateView):
    model = Project
    form_class = ProjectForm

    def get_form_kwargs(self):
        catalogs = Catalog.objects.filter_current_site() \
                                  .filter_group(self.request.user) \
                                  .filter_availability(self.request.user)

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
        tasks = Task.objects.filter_current_site() \
                            .filter_group(self.request.user) \
                            .filter_availability(self.request.user)
        for task in tasks:
            form.instance.tasks.add(task)

        # add all views to project
        views = View.objects.filter_current_site() \
                            .filter_catalog(self.object.catalog) \
                            .filter_group(self.request.user) \
                            .filter_availability(self.request.user)
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

        for import_key, import_plugin in get_plugins('PROJECT_IMPORTS').items():
            import_plugin.file_name = import_tmpfile_name

            if import_plugin.check():
                try:
                    import_plugin.process()
                except ValidationError as e:
                    return render(request, 'core/error.html', {
                        'title': _('Import error'),
                        'errors': e
                    }, status=400)

                # store information in session for ProjectCreateImportView
                request.session['create_import_tmpfile_name'] = import_tmpfile_name
                request.session['create_import_key'] = import_key

                return render(request, 'projects/project_upload.html', {
                    'create': True,
                    'file_name': uploaded_file.name,
                    'project': import_plugin.project,
                    'values': import_plugin.values,
                    'snapshots': import_plugin.snapshots,
                    'tasks': import_plugin.tasks,
                    'views': import_plugin.views
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
        import_key = request.session.get('create_import_key')
        checked = [key for key, value in request.POST.items() if 'on' in value]

        if import_tmpfile_name and import_key:
            import_plugin = get_plugin('PROJECT_IMPORTS', import_key)
            import_plugin.file_name = import_tmpfile_name

            if import_plugin.check():
                try:
                    import_plugin.process()
                except ValidationError as e:
                    return render(request, 'core/error.html', {
                        'title': _('Import error'),
                        'errors': e
                    }, status=400)

                # add current site and save project
                import_plugin.project.site = get_current_site(self.request)
                import_plugin.project.save()

                # add user to project
                membership = Membership(project=import_plugin.project, user=request.user, role='owner')
                membership.save()

                save_import_values(import_plugin.project, import_plugin.values, checked)
                save_import_snapshot_values(import_plugin.project, import_plugin.snapshots, checked)
                save_import_tasks(import_plugin.project, import_plugin.tasks)
                save_import_views(import_plugin.project, import_plugin.views)

                return HttpResponseRedirect(import_plugin.project.get_absolute_url())

        return render(request, 'core/error.html', {
            'title': _('Import error'),
            'errors': [_('There has been an error with your import.')]
        }, status=400)
