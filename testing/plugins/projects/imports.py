from django import forms
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from rest_framework.response import Response

from rdmo.projects.imports import Import


class SetImport(Import):
    label = _('Import set')
    description = _('Import into single dataset, which can be selected in a form.')

    class Form(forms.Form):
        dataset = forms.CharField(label=_('Select dataset of your project'))

        def __init__(self, *args, **kwargs):
            dataset_choices = kwargs.pop('dataset_choices')
            super().__init__(*args, **kwargs)

            self.fields['dataset'].widget = forms.RadioSelect(choices=dataset_choices)

    def get_sets(self, path):
        return (
            self.current_project.values.filter(snapshot=None, attribute__path=path)
            .order_by('set_index', 'collection_index')
        )

    def render(self):
        datasets = self.get_sets('set/id')
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
        dataset_choices = self.session.get('dataset_choices')
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
