from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from .models import Project, Snapshot, Membership


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


class UploadFileForm(forms.Form):
    uploaded_file = forms.FileField(
        label='Select a file',
    )
