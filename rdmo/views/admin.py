from django.contrib import admin

from rdmo.core.utils import get_language_fields

from .models import View


class ViewAdmin(admin.ModelAdmin):
    search_fields = ['uri'] + get_language_fields('text') + get_language_fields('help')
    list_display = ('uri', 'title', 'help')
    readonly_fields = ('uri', )


admin.site.register(View, ViewAdmin)
