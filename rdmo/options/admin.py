from django.contrib import admin

from .models import OptionSet, Option


class OptionSetAdmin(admin.ModelAdmin):
    search_fields = ('uri', )
    readonly_fields = ('uri', )


class OptionAdmin(admin.ModelAdmin):
    search_fields = ('uri', )
    readonly_fields = ('uri', 'path')


admin.site.register(OptionSet, OptionSetAdmin)
admin.site.register(Option, OptionAdmin)
