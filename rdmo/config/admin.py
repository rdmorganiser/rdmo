from django import forms
from django.contrib import admin

from rdmo.core.utils import get_language_fields

from .models import Plugin
from .validators import PluginLockedValidator, PluginUniqueURIValidator


class PluginAdminForm(forms.ModelForm):
    uri_path = forms.SlugField(required=True)

    class Meta:
        model = Plugin
        fields = [
            "python_path",
            "plugin_type",
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
            "help_lang1",
            "help_lang2",
            "help_lang3",
            "help_lang4",
            "help_lang5",
            "available",
        ]

    def clean(self):
        PluginUniqueURIValidator(self.instance)(self.cleaned_data)
        PluginLockedValidator(self.instance)(self.cleaned_data)


@admin.register(Plugin)
class PluginAdmin(admin.ModelAdmin):
    form = PluginAdminForm

    search_fields = ['uri', *get_language_fields('title'), *get_language_fields('help')]
    list_display = ('uri', 'title', 'help', 'available')
    readonly_fields = ('uri', )
    list_filter = ('available', )
    filter_horizontal = ('catalogs', 'sites', 'editors', 'groups')
