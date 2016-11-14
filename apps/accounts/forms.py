from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        additional_fields = kwargs.pop('additional_fields')
        additional_values = user.additional_values.all()

        super(ProfileForm, self).__init__(*args, **kwargs)

        # add fields and init values for the Profile model
        for additional_field in additional_fields:

            if additional_field.type == 'text':
                field = forms.CharField()
            elif additional_field.type == 'textarea':
                field = forms.CharField(widget=forms.Textarea)
            else:
                raise Exception('Unknown additional_field type.')

            field.text = additional_field.text
            field.help = additional_field.help
            field.required = additional_field.required

            self.fields[additional_field.key] = field

        for additional_field_value in additional_values:
            self.fields[additional_field.key].initial = additional_field_value.value
