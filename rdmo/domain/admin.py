from django.contrib import admin

from .models import Attribute


class AttributeAdmin(admin.ModelAdmin):
    list_display = ('uri', 'projects_count', 'values_count')
    search_fields = ('uri', )
    readonly_fields = ('uri', 'path')


admin.site.register(Attribute, AttributeAdmin)
