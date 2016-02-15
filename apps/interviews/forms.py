from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Interview


class YesNo(forms.RadioSelect):
    widget_type = 'yesno'


class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ('title', )


class GroupForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        answers = kwargs.pop('answers')
        super(GroupForm, self).__init__(*args, **kwargs)

        for question, answer in zip(questions, answers):

            # add field for the question
            if question.widget_type == 'text':
                field = forms.CharField()
            elif question.widget_type == 'textarea':
                field = forms.CharField(widget=forms.Textarea)
            elif question.widget_type == 'select':
                field = forms.ChoiceField(choices=question.options.values_list())
            elif question.widget_type == 'radio':
                field = forms.ChoiceField(choices=question.options.values_list(), widget=forms.RadioSelect)
            elif question.widget_type == 'multiselect':
                field = forms.MultipleChoiceField(choices=question.options.values_list())
            elif question.widget_type == 'checkbox':
                field = forms.MultipleChoiceField(choices=question.options.values_list(), widget=forms.CheckboxSelectMultiple)
            elif question.widget_type == 'slider':
                field = forms.CharField()
            elif question.widget_type == 'list':
                field = forms.CharField()
            elif question.widget_type == 'yesno':
                field = forms.ChoiceField(choices=((1, _('yes')), (0, _('no'))), widget=YesNo)
            else:
                raise Exception('Unknown widget type.')

            field.label = question.text_en
            #field.help_text = detail_key.help_en

            if answer:
                field.initial = answer.value

            self.fields[question.slug] = field
