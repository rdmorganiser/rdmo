from collections import defaultdict

from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext_lazy as _
from rdmo.core.imports import handle_uploaded_file
from rdmo.core.plugins import get_plugin, get_plugins
from rdmo.domain.models import Attribute
from rdmo.options.models import Option
from rdmo.questions.models import Question

from .models import Membership, Project
from .utils import (save_import_snapshot_values, save_import_tasks,
                    save_import_values, save_import_views)


class ProjectImportMixin(object):

    def get_attributes(self):
        return {attribute.uri: attribute for attribute in Attribute.objects.all()}

    def get_options(self):
        return {option.uri: option for option in Option.objects.all()}

    def get_current_values(self, current_project):
        values = current_project.values.filter(snapshot=None).select_related('attribute')

        current_values = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        for value in values:
            current_values[value.attribute.uri][value.set_index][value.collection_index] = value
        return current_values

    def get_questions(self, catalog):
        questions = Question.objects.filter(questionset__section__catalog=catalog) \
                                    .select_related('attribute') \
                                    .order_by('attribute__uri').distinct('attribute__uri')
        return {question.attribute.uri: question for question in questions}

    def upload_file(self):
        current_project = self.object

        try:
            uploaded_file = self.request.FILES['uploaded_file']
        except KeyError:
            return None
        else:
            import_tmpfile_name = handle_uploaded_file(uploaded_file)

        for import_key, import_plugin in get_plugins('PROJECT_IMPORTS').items():
            import_plugin.file_name = import_tmpfile_name
            import_plugin.current_project = current_project
            import_plugin.attributes = self.get_attributes()
            import_plugin.options = self.get_options()

            if import_plugin.check():
                try:
                    import_plugin.process()
                except ValidationError as e:
                    return render(self.request, 'core/error.html', {
                        'title': _('Import error'),
                        'errors': e
                    }, status=400)

                # store information in session for ProjectCreateImportView
                self.request.session['update_import_tmpfile_name'] = import_tmpfile_name
                self.request.session['update_import_key'] = import_key

                # attach questions and current values
                questions = self.get_questions(import_plugin.catalog)
                current_values = self.get_current_values(current_project) if current_project else {}
                for value in import_plugin.values:
                    value.question = questions.get(value.attribute.uri)
                    value.current = current_values.get(value.attribute.uri, {}) \
                                                  .get(value.set_index, {}) \
                                                  .get(value.collection_index)

                return render(self.request, 'projects/project_import.html', {
                    'method': 'import_file',
                    'current_project': current_project,
                    'source_title': uploaded_file.name,
                    'source_project': import_plugin.project,
                    'values': import_plugin.values,
                    'snapshots': import_plugin.snapshots if not current_project else None,
                    'tasks': import_plugin.tasks,
                    'views': import_plugin.views
                })

        return render(self.request, 'core/error.html', {
            'title': _('Import error'),
            'errors': [_('Files of this type cannot be imported.')]
        }, status=400)

    def import_file(self):
        current_project = self.object

        import_tmpfile_name = self.request.session.get('update_import_tmpfile_name')
        import_key = self.request.session.get('update_import_key')
        checked = [key for key, value in self.request.POST.items() if 'on' in value]

        if import_tmpfile_name and import_key:
            import_plugin = get_plugin('PROJECT_IMPORTS', import_key)
            import_plugin.file_name = import_tmpfile_name
            import_plugin.current_project = current_project
            import_plugin.attributes = self.get_attributes()
            import_plugin.options = self.get_options()

            if import_plugin.check():
                try:
                    import_plugin.process()
                except ValidationError as e:
                    return render(self.request, 'core/error.html', {
                        'title': _('Import error'),
                        'errors': e
                    }, status=400)

                # attach current values
                if current_project:
                    current_values = self.get_current_values(current_project)
                    for value in import_plugin.values:
                        value.current = current_values.get(value.attribute.uri, {}) \
                                                      .get(value.set_index, {}) \
                                                      .get(value.collection_index)

                    save_import_values(self.object, import_plugin.values, checked)
                    save_import_tasks(self.object, import_plugin.tasks)
                    save_import_views(self.object, import_plugin.views)

                    return HttpResponseRedirect(current_project.get_absolute_url())

                else:
                    # add current site and save project
                    import_plugin.project.site = get_current_site(self.request)
                    import_plugin.project.save()

                    # add user to project
                    membership = Membership(project=import_plugin.project, user=self.request.user, role='owner')
                    membership.save()

                    for value in import_plugin.values:
                        value.current = None

                    save_import_values(import_plugin.project, import_plugin.values, checked)
                    save_import_snapshot_values(import_plugin.project, import_plugin.snapshots, checked)
                    save_import_tasks(import_plugin.project, import_plugin.tasks)
                    save_import_views(import_plugin.project, import_plugin.views)

                    return HttpResponseRedirect(import_plugin.project.get_absolute_url())

    def import_project(self):
        current_project = self.object

        # get the original project
        project = get_object_or_404(Project.objects.all(), id=self.request.POST.get('source'))

        # check if the user has the permission to access the original project
        if not self.request.user.has_perm('projects.view_project_object', project):
            self.handle_no_permission()

        values = project.values.filter(snapshot=None) \
                               .select_related('attribute', 'option')

        # attach questions and current values
        questions = self.get_questions(current_project.catalog)
        current_values = self.get_current_values(current_project)
        for value in values:
            value.question = questions.get(value.attribute.uri)
            value.current = current_values.get(value.attribute.uri, {}) \
                                          .get(value.set_index, {}) \
                                          .get(value.collection_index)
            value.file_import = False

        checked = [key for key, value in self.request.POST.items() if 'on' in value]
        if checked:
            save_import_values(current_project, values, checked)
            return HttpResponseRedirect(current_project.get_absolute_url())

        else:
            return render(self.request, 'projects/project_import.html', {
                'method': 'import_project',
                'source': project.id,
                'source_title': project.title,
                'current_project': current_project,
                'values': values,
            })
