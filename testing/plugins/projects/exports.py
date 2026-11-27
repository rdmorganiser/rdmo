from django import forms
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from rest_framework.response import Response

from rdmo.projects.exports import Export


class SetExportForm(forms.Form):
    dataset = forms.CharField(label=_('Select dataset of your project'))

    def __init__(self, *args, **kwargs):
        dataset_choices = kwargs.pop('dataset_choices')
        super().__init__(*args, **kwargs)

        self.fields['dataset'].widget = forms.RadioSelect(choices=dataset_choices)


class SetExport(Export):
    label = _('Dataset')
    description = _('Export a single dataset of the project, which can be selected in a form.')

    def render(self):
        datasets = self.get_set('set/id')
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
        dataset_choices = self.session.get('dataset_choices')
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
