from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from rdmo.core.plugins import get_plugin

from .models import (Integration, IntegrationOption, Membership, Project,
                     Snapshot)


class CatalogChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return mark_safe('<b>%s</b></br>%s' % (obj.title, obj.help))


class TasksMultipleChoiceField(forms.ModelMultipleChoiceField):

    def label_from_instance(self, obj):
        return mark_safe('<b>%s</b></br>%s' % (obj.title, obj.text))


class ViewsMultipleChoiceField(forms.ModelMultipleChoiceField):

    def label_from_instance(self, obj):
        return mark_safe('<b>%s</b></br>%s' % (obj.title, obj.help))


class ProjectForm(forms.ModelForm):

    use_required_attribute = False

    def __init__(self, *args, **kwargs):
        catalogs = kwargs.pop('catalogs')
        super().__init__(*args, **kwargs)
        self.fields['catalog'].queryset = catalogs
        self.fields['catalog'].empty_label = None

    class Meta:
        model = Project
        fields = ('title', 'description', 'catalog')
        field_classes = {
            'catalog': CatalogChoiceField
        }
        widgets = {
            'catalog': forms.RadioSelect()
        }


class ProjectTasksForm(forms.ModelForm):

    use_required_attribute = False

    def __init__(self, *args, **kwargs):
        tasks = kwargs.pop('tasks')
        super().__init__(*args, **kwargs)

        self.fields['tasks'].queryset = tasks

    class Meta:
        model = Project
        fields = ('tasks', )
        field_classes = {
            'tasks': TasksMultipleChoiceField
        }
        widgets = {
            'tasks': forms.CheckboxSelectMultiple()
        }


class ProjectViewsForm(forms.ModelForm):

    use_required_attribute = False

    def __init__(self, *args, **kwargs):
        views = kwargs.pop('views')
        super().__init__(*args, **kwargs)

        self.fields['views'].queryset = views

    class Meta:
        model = Project
        fields = ('views', )
        field_classes = {
            'views': ViewsMultipleChoiceField
        }
        widgets = {
            'views': forms.CheckboxSelectMultiple()
        }


class SnapshotCreateForm(forms.ModelForm):

    use_required_attribute = False

    class Meta:
        model = Snapshot
        fields = ('title', 'description')

    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project')
        super(SnapshotCreateForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.project = self.project
        return super(SnapshotCreateForm, self).save(*args, **kwargs)


class MembershipCreateForm(forms.ModelForm):

    use_required_attribute = False

    class Meta:
        model = Membership
        fields = ('role', )

    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project')

        super(MembershipCreateForm, self).__init__(*args, **kwargs)

        self.fields['username_or_email'] = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Username or email')}))
        self.fields['username_or_email'].label = _('User')
        self.fields['username_or_email'].help_text = _('The username or email for the user of this membership.')

        self.order_fields(('username_or_email', 'role'))

    def clean_username_or_email(self):
        username_or_email = self.cleaned_data['username_or_email']
        try:
            self.cleaned_data['user'] = User.objects.get(Q(username=username_or_email) | Q(email=username_or_email))
        except User.DoesNotExist:
            raise ValidationError(_('Please enter a valid username or email.'))

        if self.cleaned_data['user'] in self.project.user.all():
            raise ValidationError(_('The user is already a member of the project.'))

    def save(self, *args, **kwargs):
        self.instance.project = self.project
        self.instance.user = self.cleaned_data['user']
        return super(MembershipCreateForm, self).save(*args, **kwargs)


class IntegrationForm(forms.ModelForm):

    class Meta:
        model = Integration
        fields = ()

    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project')
        self.provider_key = kwargs.pop('provider_key', None)
        super().__init__(*args, **kwargs)

        # get the provider
        if self.provider_key:
            self.provider = get_plugin('SERVICE_PROVIDERS', self.provider_key)
        else:
            self.provider = self.instance.provider

        # add fields for the integration options
        for field in self.provider.fields:
            try:
                initial = IntegrationOption.objects.get(integration=self.instance, key=field.get('key')).value
            except IntegrationOption.DoesNotExist:
                initial = None

            if field.get('placeholder'):
                attrs = {'placeholder': field.get('placeholder')}
            self.fields[field.get('key')] = forms.CharField(widget=forms.TextInput(attrs=attrs),
                                                            initial=initial, required=field.get('required', True))

    def save(self):
        # the the project and the provider_key
        self.instance.project = self.project
        if self.provider_key:
            self.instance.provider_key = self.provider_key

        # call the form's save method
        super().save()

        # save the integration options
        self.instance.save_options(self.cleaned_data)


class IssueSendForm(forms.Form):

    class AttachmentViewsField(forms.ModelMultipleChoiceField):
        def label_from_instance(self, obj):
            return _('Attach %s') % obj.title

    class AttachmentSnapshotField(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return obj.title

    subject = forms.CharField(label=_('Subject'), max_length=128)
    message = forms.CharField(label=_('Message'), widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project')
        super().__init__(*args, **kwargs)

        self.fields['attachments_answers'] = forms.MultipleChoiceField(
            label=_('Answers'), widget=forms.CheckboxSelectMultiple, required=False,
            choices=[('project_answers', _('Attach the output of "View answers".'))]
        )
        self.fields['attachments_views'] = self.AttachmentViewsField(
            label=_('Views'), widget=forms.CheckboxSelectMultiple, required=False,
            queryset=self.project.views.all(), to_field_name='id'
        )
        self.fields['attachments_snapshot'] = self.AttachmentSnapshotField(
            label=_('Snapshot'), widget=forms.RadioSelect, required=False,
            queryset=self.project.snapshots.all(), empty_label=_('Current')
        )
        self.fields['attachments_format'] = forms.ChoiceField(
            label=_('Format'), widget=forms.RadioSelect, required=False,
            choices=settings.EXPORT_FORMATS
        )

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get('attachments_answers') or cleaned_data.get('attachments_views'):
            if not cleaned_data.get('attachments_format'):
                self.add_error('attachments_format', _('This field is required.'))


class IssueMailForm(forms.Form):

    if settings.EMAIL_RECIPIENTS_CHOICES:
        recipients = forms.MultipleChoiceField(label=_('Recipients'), widget=forms.CheckboxSelectMultiple,
                                               required=not settings.EMAIL_RECIPIENTS_INPUT,
                                               choices=settings.EMAIL_RECIPIENTS_CHOICES)

    if settings.EMAIL_RECIPIENTS_INPUT:
        recipients_input = forms.CharField(label=_('Recipients'), widget=forms.Textarea(attrs={
            'placeholder': _('Enter recipients line by line')
        }), required=not settings.EMAIL_RECIPIENTS_CHOICES)

    def clean(self):
        cleaned_data = super().clean()

        if settings.EMAIL_RECIPIENTS_INPUT and \
                cleaned_data.get('recipients') == [] and \
                cleaned_data.get('recipients_input') == []:
            self.add_error('recipients_input', _('This field is required.'))

    def clean_recipients_input(self):
        email_validator = EmailValidator()
        cleaned_data = []

        for line in self.cleaned_data['recipients_input'].splitlines():
            email = line.strip()
            email_validator(email)
            cleaned_data.append(email)

        return cleaned_data


class UploadFileForm(forms.Form):
    uploaded_file = forms.FileField(
        label='Select a file',
    )
