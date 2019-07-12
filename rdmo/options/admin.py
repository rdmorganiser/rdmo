from django.contrib import admin

from rdmo.core.utils import get_language_fields

from .models import OptionSet, Option


class OptionSetAdmin(admin.ModelAdmin):
    search_fields = ('uri', )
    readonly_fields = ('uri', )


class OptionAdmin(admin.ModelAdmin):
    search_fields = ['uri'] + get_language_fields('text')
    list_display = ('uri', 'text', 'additional_input')
    readonly_fields = ('uri', 'path')
    list_filter = ('optionset', 'additional_input')


admin.site.register(OptionSet, OptionSetAdmin)
admin.site.register(Option, OptionAdmin)
