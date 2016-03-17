from django import forms
from django.utils.translation import ugettext_lazy as _


class YesNo(forms.RadioSelect):
    widget_type = 'yesno'


class QuestionEntityForm(forms.Form):
    def add_field(self, question, value, index=None):
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
        field.initial = value.text

        if index is not None:
            self.fields['%s[%i]' % (question.tag, index)] = field
        else:
            self.fields[question.tag] = field


class QuestionSetForm(QuestionEntityForm):
    def __init__(self, *args, **kwargs):
        questionset = kwargs.pop('questionset')
        valuesets = kwargs.pop('valuesets')

        super(QuestionSetForm, self).__init__(*args, **kwargs)

        for valueset in valuesets:
            for question, value in zip(questionset.questions.all(), valueset.values.all()):
                self.add_field(question, value, index=valueset.index)


class QuestionForm(QuestionEntityForm):
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        value = kwargs.pop('value')

        super(QuestionForm, self).__init__(*args, **kwargs)

        self.add_field(question, value)
