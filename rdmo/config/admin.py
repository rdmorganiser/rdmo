from django.contrib import admin

from rdmo.core.utils import get_language_fields

from .models import Plugin
from .validators import PluginLockedValidator, PluginUniqueURIValidator
from rdmo.core.admin import ElementAdminForm


class PluginAdminForm(ElementAdminForm):

    class Meta:
        model = Plugin
        fields = '__all__'

    def clean(self):
        PluginUniqueURIValidator(self.instance)(self.cleaned_data)
        PluginLockedValidator(self.instance)(self.cleaned_data)



@admin.register(Plugin)
class PluginAdmin(admin.ModelAdmin):
    form = PluginAdminForm

    search_fields = ['uri', 'python_path', *get_language_fields('title'), *get_language_fields('help')]
    list_display = ('uri', 'python_path', 'title', 'available')
    readonly_fields = ('uri', )
    list_filter = ('available', 'python_path')
    filter_horizontal = ('catalogs', 'sites', 'editors', 'groups')
