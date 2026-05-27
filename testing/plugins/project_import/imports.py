from django import forms
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

import requests

from rdmo.core.imports import handle_fetched_file
from rdmo.projects.imports import Import, RDMOXMLImport
from rdmo.projects.models import Project


class SimpleImportPlugin(Import):

    accept = {"text/plain": [".txt"]}
    default_uri_prefix = "https://rdmorganiser.github.io/terms"
    url_name = "simple"

    def check(self) -> bool:
        # Approve files ending with .txt
        return str(self.file_name).endswith(".txt")

    def process(self):
        # Create a new Project for testing.  You could populate values/tasks/etc.
        self.project = Project(title="Imported test project")


class SimpleURLImportPlugin(RDMOXMLImport):

    accept = False
    upload = False

    class Form(forms.Form):
        url = forms.URLField(label=_('Import project from this URL'), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.provider = RDMOXMLImport(*args, **kwargs)

    def render(self):
        form = self.Form()
        return render(self.request, 'projects/project_import_form.html', {
            'source_title': 'URL',
            'form': form
        }, status=200)

    def submit(self):
        form = self.Form(self.request.POST)

        if 'cancel' in self.request.POST:
            if self.project is None:
                return redirect('projects')
            else:
                return redirect('project', self.project.id)

        if form.is_valid():
            self.source_title = form.cleaned_data['url']

            response = requests.get(form.cleaned_data['url'])
            self.request.session['import_file_name'] = handle_fetched_file(response.content)

            if self.current_project:
                return redirect('project_update_import', self.current_project.id)
            else:
                return redirect('project_create_import')

        return render(self.request, 'projects/project_import_form.html', {
            'source_title': 'URL',
            'form': form
        }, status=200)
