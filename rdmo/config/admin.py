from django import forms
from django.contrib import admin

from rdmo.core.admin import ElementAdminForm
from rdmo.core.utils import get_language_fields, get_plugin_python_paths

from .models import Plugin
from .validators import PluginLockedValidator, PluginPythonPathValidator, PluginUniqueURIValidator


class PluginAdminForm(ElementAdminForm):

    python_path = forms.ChoiceField(choices=[(plugin, plugin) for plugin in get_plugin_python_paths()])


    class Meta:
        model = Plugin
        fields = '__all__'

    def clean(self):
        PluginUniqueURIValidator(self.instance)(self.cleaned_data)
        PluginLockedValidator(self.instance)(self.cleaned_data)
        PluginPythonPathValidator(self.instance)(self.cleaned_data)



@admin.register(Plugin)
class PluginAdmin(admin.ModelAdmin):
    form = PluginAdminForm

    search_fields = ['uri', 'python_path', *get_language_fields('title'), *get_language_fields('help')]
    list_display = ('uri', 'python_path', 'plugin_type', 'available')
    readonly_fields = ('uri', 'plugin_type')
    list_filter = ('available', 'python_path', 'sites' , 'groups', 'catalogs')
    filter_horizontal = ('catalogs', 'sites', 'editors', 'groups')
    ordering = ('python_path','order')
