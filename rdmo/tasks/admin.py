from django import forms
from django.contrib import admin

from rdmo.core.utils import get_language_fields

from .models import Task
from .validators import TaskLockedValidator, TaskUniqueURIValidator


class TaskAdminForm(forms.ModelForm):
    uri_path = forms.SlugField(required=True)

    class Meta:
        model = Task
        fields = [
            "uri",
            "uri_prefix",
            "uri_path",
            "comment",
            "locked",
            "catalogs",
            "sites",
            "editors",
            "groups",
            "title_lang1",
            "title_lang2",
            "title_lang3",
            "title_lang4",
            "title_lang5",
            "text_lang1",
            "text_lang2",
            "text_lang3",
            "text_lang4",
            "text_lang5",
            "start_attribute",
            "end_attribute",
            "days_before",
            "days_after",
            "conditions",
            "available",
        ]

    def clean(self):
        TaskUniqueURIValidator(self.instance)(self.cleaned_data)
        TaskLockedValidator(self.instance)(self.cleaned_data)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    form = TaskAdminForm

    search_fields = ['uri', *get_language_fields('title'), *get_language_fields('text')]
    list_display = ('uri', 'title', 'text', 'available')
    readonly_fields = ('uri', )
    list_filter = ('available', )
    filter_horizontal = ('catalogs', 'sites', 'editors', 'groups', 'conditions')
