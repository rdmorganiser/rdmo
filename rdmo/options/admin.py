from django.contrib import admin

from .models import OptionSet, Option


class OptionSetAdmin(admin.ModelAdmin):
    search_fields = ('uri', )
    readonly_fields = ('uri', )


class OptionAdmin(admin.ModelAdmin):
    search_fields = ('uri', 'text_en', 'text_de')
    list_display = ('uri', 'text', 'additional_input')
    readonly_fields = ('uri', 'path')


admin.site.register(OptionSet, OptionSetAdmin)
admin.site.register(Option, OptionAdmin)
