from django.contrib import admin

from .models import Task


class TaskAdmin(admin.ModelAdmin):
    search_fields = ('uri', )
    readonly_fields = ('uri', )


admin.site.register(Task, TaskAdmin)
