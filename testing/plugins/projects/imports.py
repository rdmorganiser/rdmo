from django import forms
from django.conf import settings
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

import requests

from rdmo.core.plugins import PluginResponse, PluginSession
from rdmo.projects.imports import Import
from rdmo.projects.imports.utils import create_project
from rdmo.projects.plugins import ProjectValues
from rdmo.services.client import OauthClient
from rdmo.services.exceptions import OauthAuthorizationRequired


class SetImport(Import):
    label = _('Import set')
    description = _('Import into single dataset, which can be selected in a form.')

    class Form(forms.Form):
        dataset = forms.CharField(label=_('Select dataset of your project'))

        def __init__(self, *args, **kwargs):
            dataset_choices = kwargs.pop('dataset_choices')
            super().__init__(*args, **kwargs)

            self.fields['dataset'].widget = forms.RadioSelect(choices=dataset_choices)

    @property
    def session(self):
        return PluginSession(self)

    @property
    def response(self):
        return PluginResponse(self)

    @cached_property
    def values(self):
        return ProjectValues(self.current_project)

    def render(self):
        datasets = self.values.get_set('set/id') if self.current_project else []
        dataset_choices = [(dataset.set_index, dataset.value) for dataset in datasets]
        self.session.set('dataset_choices', dataset_choices)

        form = self.Form(dataset_choices=dataset_choices)

        return self.response.html('plugins/form.html', {
            'form': form,
            'submit_label': _('Import'),
        })

    def submit(self):
        dataset_choices = self.session.get('dataset_choices', [])
        form = self.Form(self.request.POST, dataset_choices=dataset_choices)

        if 'cancel' in self.request.POST:
            return self.response.success()

        if form.is_valid():
            return self.response.success()

        return self.response.html('plugins/form.html', {
            'form': form,
            'submit_label': _('Import'),
        })


class URLImport(Import):
    label = _('Import from URL')
    description = _('Import answers from an URL.')

    class Form(forms.Form):
        url = forms.URLField(label=_('Import answers from this URL'), required=True)

    @property
    def response(self):
        return PluginResponse(self)

    def render(self):
        form = self.Form()
        return self.response.html('plugins/form.html', {
            'form': form,
            'submit_label': _('Import'),
        })

    def submit(self):
        form = self.Form(self.request.POST)

        if 'cancel' in self.request.POST:
            return self.response.success()

        if form.is_valid():
            return self.response.success()

        return self.response.html('plugins/form.html', {
            'form': form,
            'submit_label': _('Import'),
        })


class OAuthImport(Import):
    label = _('Import from external service')
    description = _('Import the title and description of the project from an external service.')

    @property
    def client(self):
        return OauthClient(self, **settings.OAUTH_PROVIDER)

    @property
    def session(self):
        return PluginSession(self)

    @property
    def response(self):
        return PluginResponse(self)

    @property
    def next_url(self):
        if self.current_project is None:
            return reverse('projects_import', args=[self.key])
        else:
            return reverse('project_import', args=[self.current_project.id, self.key])

    def render(self):
        try:
            project = self.fetch_project()
        except OauthAuthorizationRequired:
            return self.client.redirect(self.next_url)
        except (requests.RequestException, ValueError) as e:
            raise self.response.error({
                'external_service': [_('The request to the external service failed: %s') % e]
            }) from e

        self.session.set('project', project)

        return self.response.html('plugins/form.html', {
            'project': project,
            'submit_label': _('Import'),
        })

    def submit(self):
        if 'cancel' in self.request.POST:
            self.session.pop('project')
            return self.response.success()

        project = self.session.pop('project')
        if project is None:
            raise self.response.error({'project': [_('Please fetch the data from the service first.')]})

        if self.current_project is None:
            new_project = create_project(
                self.request,
                title=project.get('title') or _('Imported project'),
                description=project.get('description') or '',
                catalog_uri=project.get('catalog')
            )
            return self.response.redirect(reverse('project', args=[new_project.id]))

        # keep the current values, if the service does not provide them
        self.current_project.title = project.get('title') or self.current_project.title
        self.current_project.description = project.get('description') or self.current_project.description
        self.current_project.save()

        return self.response.success()

    def fetch_project(self):
        response = self.client.get(settings.OAUTH_PROVIDER_URL)
        response.raise_for_status()

        project = response.json().get('project')
        return project if isinstance(project, dict) else {}
