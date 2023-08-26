from django import forms
from django.contrib import admin

from rdmo.core.utils import get_language_fields

from .models import Task
from .validators import TaskLockedValidator, TaskUniqueURIValidator


class TaskAdminForm(forms.ModelForm):
    uri_path = forms.SlugField(required=True)

    class Meta:
        model = Task
        fields = '__all__'

    def clean(self):
        TaskUniqueURIValidator(self.instance)(self.cleaned_data)
        TaskLockedValidator(self.instance)(self.cleaned_data)


class TaskAdmin(admin.ModelAdmin):
    form = TaskAdminForm

    search_fields = ['uri', *get_language_fields('title'), *get_language_fields('text')]
    list_display = ('uri', 'title', 'text', 'available')
    readonly_fields = ('uri', )
    list_filter = ('available', )
    filter_horizontal = ('catalogs', 'sites', 'editors', 'groups', 'conditions')


admin.site.register(Task, TaskAdmin)
