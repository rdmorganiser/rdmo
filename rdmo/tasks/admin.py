from django.contrib import admin

from rdmo.core.utils import get_language_fields

from .models import Task


class TaskAdmin(admin.ModelAdmin):
    search_fields = ['uri'] + get_language_fields('title') + get_language_fields('help')
    list_display = ('uri', 'title', 'text')
    readonly_fields = ('uri', )


admin.site.register(Task, TaskAdmin)
