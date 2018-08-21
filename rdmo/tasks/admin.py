from django.contrib import admin

from .models import Task, TimeFrame


class TaskAdmin(admin.ModelAdmin):
    search_fields = ('uri', 'title_en', 'title_de', 'text_en', 'text_de')
    list_display = ('uri', 'title', 'text')
    readonly_fields = ('uri', )


class TimeFrameAdmin(admin.ModelAdmin):
    search_fields = ('task__uri', )
    list_display = ('task', 'start_attribute', 'end_attribute')


admin.site.register(Task, TaskAdmin)
admin.site.register(TimeFrame, TimeFrameAdmin)
