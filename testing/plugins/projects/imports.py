from django import forms
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from rest_framework.response import Response

from rdmo.core.plugins import PluginSession
from rdmo.projects.imports import Import
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

    @cached_property
    def values(self):
        return ProjectValues(self.current_project)

    def render(self):
        datasets = self.values.get_set('set/id') if self.current_project else []
        dataset_choices = [(dataset.set_index, dataset.value) for dataset in datasets]
        self.session.set('dataset_choices', dataset_choices)

        form = self.Form(dataset_choices=dataset_choices)

        return Response({
            'html': render_to_string('plugins/form.html', {
                'form': form,
                'submit_label': _('Import'),
            },
            request=self.request)
        })

    def submit(self):
        dataset_choices = self.session.get('dataset_choices', [])
        form = self.Form(self.request.POST, dataset_choices=dataset_choices)

        if 'cancel' in self.request.POST:
            return Response({'location': {'area': 'transfer'}})

        if form.is_valid():
            return Response({'location': {'area': 'dashboard'}})

        return Response({
            'html': render_to_string('plugins/form.html', {
                'form': form,
                'submit_label': _('Import'),
            },
            request=self.request)
        })


class URLImport(Import):
    label = _('Import from URL')
    description = _('Import answers from an URL.')

    class Form(forms.Form):
        url = forms.URLField(label=_('Import answers from this URL'), required=True)

    def render(self):
        form = self.Form()
        return Response({
            'html': render_to_string('plugins/form.html', {
                'form': form,
                'submit_label': _('Import'),
            },
            request=self.request)
        })

    def submit(self):
        form = self.Form(self.request.POST)

        if 'cancel' in self.request.POST:
            return Response({'location': {'area': 'transfer'}})

        if form.is_valid():
            return Response({'location': {'area': 'dashboard'}})

        return Response({
            'html': render_to_string('plugins/form.html', {
                'form': form,
                'submit_label': _('Import'),
            },
            request=self.request)
        })


class OAuthImport(Import):
    label = _('Import from external service')
    description = _('Import answers from an external service.')

    @property
    def client(self):
        return OauthClient(self, **settings.OAUTH_PROVIDER)

    @property
    def next_url(self):
        return reverse('project', args=[self.current_project.id]) + f'transfer/import/{self.key}/'

    def render(self):
        try:
            response = self.client.get(settings.OAUTH_PROVIDER_URL)
            response.raise_for_status()
        except OauthAuthorizationRequired:
            return self.client.redirect(self.next_url)

        project = response.json().get('project', {})

        return Response({
            'html': render_to_string('plugins/form.html', {
                'project': project,
                'submit_label': _('Import'),
            },
            request=self.request)
        })

    def submit(self):
        if 'cancel' in self.request.POST:
            return Response({'location': {'area': 'transfer'}})

        try:
            response = self.client.get(settings.OAUTH_PROVIDER_URL)
            response.raise_for_status()
        except OauthAuthorizationRequired:
            return self.client.redirect(self.next_url)

        project = response.json().get('project', {})

        self.current_project.title = project.get('title')
        self.current_project.description = project.get('description')
        self.current_project.save()

        return Response({'location': {'area': 'transfer'}})
