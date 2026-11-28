from django import forms
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from rest_framework.response import Response

from rdmo.core.plugins import PluginSession
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

    @cached_property
    def values(self):
        return ProjectValues(self.project, self.snapshot)

    def render(self):
        datasets = self.values.get_set('set/id')
        dataset_choices = [(dataset.set_index, dataset.value)for dataset in datasets]

        self.session.set('dataset_choices', dataset_choices)

        form = SetExportForm(dataset_choices=dataset_choices)

        return Response({
            'html': render_to_string('plugins/form.html', {
                'form': form,
                'submit_label': _('Export'),
            },
            request=self.request)
        })

    def submit(self):
        dataset_choices = self.session.get('dataset_choices', [])
        form = SetExportForm(self.request.POST, dataset_choices=dataset_choices)

        if 'cancel' in self.request.POST:
            return Response({'location': {'area': 'transfer'}})

        if form.is_valid():
            return Response({'location': {'area': 'dashboard'}})

        return Response({
            'html': render_to_string('plugins/form.html', {
                'form': form,
                'submit_label': _('Export'),
            },
            request=self.request)
        })


class OAuthExport(Export):
    label = _('Export to external service')
    description = _('Export the title and description of the project to an external service.')

    @property
    def client(self):
        return OauthClient(self, **settings.OAUTH_PROVIDER)

    @property
    def next_url(self):
        return reverse('project', args=[self.project.id]) + f'transfer/export/{self.key}/'

    def render(self):
        try:
            self.client.get(settings.OAUTH_PROVIDER_URL).raise_for_status()
        except OauthAuthorizationRequired:
            return self.client.redirect(self.next_url)

        return Response({
            'html': render_to_string('plugins/form.html', {
                'project': self.project,
                'submit_label': _('Export'),
            },
            request=self.request)
        })

    def submit(self):
        if 'cancel' in self.request.POST:
            return Response({'location': {'area': 'transfer'}})

        try:
            self.client.post(settings.OAUTH_PROVIDER_URL, json={}).raise_for_status()
        except OauthAuthorizationRequired:
            return self.client.redirect(self.next_url)

        return Response({'location': {'area': 'transfer'}})
