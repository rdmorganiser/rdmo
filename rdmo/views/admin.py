from django.contrib import admin

from .models import View


class ViewAdmin(admin.ModelAdmin):
    search_fields = ('uri', 'title_en', 'title_de', 'help_en', 'help_de')
    list_display = ('uri', 'title', 'help')
    readonly_fields = ('uri', )


admin.site.register(View, ViewAdmin)
