from django import forms
from django.utils.translation import ugettext_lazy as _

class UpdateProfile(forms.Form):

    next = forms.CharField(widget=forms.HiddenInput(), required=False)
    username = forms.CharField(label=_('Username'))
    email = forms.EmailField(label=_('Email'))
    first_name = forms.CharField(label=_('First name'))
    last_name = forms.CharField(label=_('Last name'))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        detail_keys = kwargs.pop('detail_keys')
        next = kwargs.pop('next')

        super(UpdateProfile, self).__init__(*args, **kwargs)

        # set hidden next field
        self.fields['next'].initial = next

        # set inital values for the User model
        self.fields['username'].initial = user.username
        self.fields['email'].initial = user.email
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name

        # add fields and init values for the Profile model
        for detail_key in detail_keys:
            if detail_key.type == 'text':
                field = forms.CharField()
            elif detail_key.type == 'textarea':
                field = forms.CharField(widget=forms.Textarea)
            elif detail_key.type == 'select':
                field = forms.ChoiceField(choices=detail_key.options)
            elif detail_key.type == 'radio':
                field = forms.ChoiceField(choices=detail_key.options, widget=forms.RadioSelect)
            elif detail_key.type == 'multiselect':
                field = forms.MultipleChoiceField(choices=detail_key.options)
            elif detail_key.type == 'checkbox':
                field = forms.MultipleChoiceField(choices=detail_key.options, widget=forms.CheckboxSelectMultiple)
            else:
                raise Exception('Unknown detail key type.')

            field.label = detail_key.label
            field.required = detail_key.required
            field.help_text = detail_key.help_text
            self.fields[detail_key.key] = field

            # add an initial value, if one is found in the user details
            if user.profile.details and detail_key.key in user.profile.details:
                self.fields[detail_key.key].initial = user.profile.details[detail_key.key]
