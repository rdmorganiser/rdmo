from django.contrib import admin

from .models import Task


class TaskAdmin(admin.ModelAdmin):
    search_fields = ('uri', 'title_en', 'title_de', 'text_en', 'text_de')
    list_display = ('uri', 'title', 'text')
    readonly_fields = ('uri', )


admin.site.register(Task, TaskAdmin)
