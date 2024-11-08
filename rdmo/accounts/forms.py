import logging

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from allauth.account.forms import LoginForm as AllauthLoginForm
from allauth.account.forms import SignupForm as AllauthSignupForm

from .models import AdditionalField, AdditionalFieldValue, ConsentFieldValue

log = logging.getLogger(__name__)


class ProfileForm(forms.ModelForm):

    use_required_attribute = False

    class Meta:
        model = get_user_model()
        if settings.ACCOUNT:
            fields = ('first_name', 'last_name')
        else:
            fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget = forms.TextInput(attrs={'placeholder': _('First name')})
        self.fields['last_name'].widget = forms.TextInput(attrs={'placeholder': _('Last name')})

        self.additional_fields = AdditionalField.objects.all()

        # add fields and init values for the Profile model
        for additional_field in self.additional_fields:

            if additional_field.type == 'text':
                field = forms.CharField(widget=forms.TextInput(attrs={'placeholder': additional_field.text}))
            elif additional_field.type == 'textarea':
                field = forms.CharField(widget=forms.Textarea(attrs={'placeholder': additional_field.text}))
            else:
                raise Exception('Unknown additional_field type.')

            field.label = additional_field.text
            field.help = additional_field.help
            field.required = additional_field.required

            self.fields[additional_field.key] = field

        # existing user is going to be updated
        if self.instance.pk is not None:
            for additional_field_value in AdditionalFieldValue.objects.filter(user=self.instance):
                self.fields[additional_field_value.field.key].initial = additional_field_value.value

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._save_additional_values()

    def _save_additional_values(self, user=None):
        if user is None:
            user = self.instance

        for additional_field in self.additional_fields:
            try:
                additional_value = user.additional_values.get(field=additional_field)
            except AdditionalFieldValue.DoesNotExist:
                additional_value = AdditionalFieldValue(user=user, field=additional_field)

            additional_value.value = self.cleaned_data[additional_field.key]
            additional_value.save()


class LoginForm(AllauthLoginForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # remove forget password link introduced with allauth 0.57.0
        password_field = self.fields.get('password')
        if password_field:
            password_field.help_text = None


class SignupForm(AllauthSignupForm, ProfileForm):

    use_required_attribute = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # add a consent field, the label is added in the template
        if settings.ACCOUNT_TERMS_OF_USE:
            self.fields['consent'] = forms.BooleanField(required=True)

    def signup(self, request, user):
        self._save_additional_values(user)

        # store the consent field
        if settings.ACCOUNT_TERMS_OF_USE:
            consent = ConsentFieldValue(user=user, consent=self.cleaned_data['consent'])
            consent.save()


class RemoveForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        if not self.request.user.has_usable_password():
            self.fields.pop('password')

    email = forms.CharField(widget=forms.TextInput(attrs={'required': 'false'}))
    email.label = _('E-mail')
    email.widget.attrs = {'class': 'form-control', 'placeholder': email.label}

    password = forms.CharField(widget=forms.PasswordInput)
    password.label = _('Password')
    password.widget.attrs = {'class': 'form-control', 'placeholder': password.label}

    consent = forms.BooleanField(required=True)
    consent.label = _("I confirm that I want my profile to be completely removed. This can not be undone!")
