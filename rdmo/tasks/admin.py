from django.contrib import admin

from .models import Task, TimeFrame


class TaskAdmin(admin.ModelAdmin):
    search_fields = ('uri', )
    readonly_fields = ('uri', )


class TimeFrameAdmin(admin.ModelAdmin):
    search_fields = ('task_uri', )


admin.site.register(Task, TaskAdmin)
admin.site.register(TimeFrame, TimeFrameAdmin)
