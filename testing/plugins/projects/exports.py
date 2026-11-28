from django import forms
from django.conf import settings
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

import requests

from rdmo.core.plugins import PluginResponse, PluginSession
from rdmo.projects.exports import Export
from rdmo.projects.plugins import ProjectValues
from rdmo.services.client import OauthClient
from rdmo.services.exceptions import OauthAuthorizationRequired


class SetExportForm(forms.Form):
    dataset = forms.CharField(label=_('Select dataset of your project'))

    def __init__(self, *args, **kwargs):
        dataset_choices = kwargs.pop('dataset_choices')
        super().__init__(*args, **kwargs)

        self.fields['dataset'].widget = forms.RadioSelect(choices=dataset_choices)


class SetExport(Export):
    label = _('Dataset')
    description = _('Export a single dataset of the project, which can be selected in a form.')

    @property
    def session(self):
        return PluginSession(self)

    @property
    def response(self):
        return PluginResponse(self)

    @cached_property
    def values(self):
        return ProjectValues(self.project, self.snapshot)

    def render(self):
        datasets = self.values.get_set('set/id')
        dataset_choices = [(dataset.set_index, dataset.value)for dataset in datasets]

        self.session.set('dataset_choices', dataset_choices)

        form = SetExportForm(dataset_choices=dataset_choices)

        return self.response.html('plugins/form.html', {
            'form': form,
            'submit_label': _('Export'),
        })

    def submit(self):
        dataset_choices = self.session.get('dataset_choices', [])
        form = SetExportForm(self.request.POST, dataset_choices=dataset_choices)

        if 'cancel' in self.request.POST:
            return self.response.success()

        if form.is_valid():
            return self.response.success()

        return self.response.html('plugins/form.html', {
            'form': form,
            'submit_label': _('Export'),
        })


class OAuthExport(Export):
    label = _('Export to external service')
    description = _('Export the title and description of the project to an external service.')

    @property
    def client(self):
        return OauthClient(self, **settings.OAUTH_PROVIDER)

    @property
    def response(self):
        return PluginResponse(self)

    @property
    def next_url(self):
        return reverse('project_export', args=[self.project.id, self.key])

    def render(self):
        try:
            self.client.get(settings.OAUTH_PROVIDER_URL).raise_for_status()
        except OauthAuthorizationRequired:
            return self.client.redirect(self.next_url)
        except (requests.RequestException, ValueError) as e:
            raise self.response.error({
                'external_service': [_('The request to the external service failed: %s') % e]
            }) from e

        return self.response.html('plugins/form.html', {
            'project': self.project,
            'submit_label': _('Export'),
        })

    def submit(self):
        if 'cancel' in self.request.POST:
            return self.response.success()

        try:
            self.client.post(settings.OAUTH_PROVIDER_URL, json={
                'title': self.project.title,
                'description': self.project.description
            }).raise_for_status()
        except OauthAuthorizationRequired:
            return self.client.redirect(self.next_url)
        except (requests.RequestException, ValueError) as e:
            raise self.response.error({
                'external_service': [_('The request to the external service failed: %s') % e]
            }) from e

        return self.response.success()
