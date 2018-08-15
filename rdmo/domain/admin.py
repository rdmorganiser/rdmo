from django.contrib import admin

from .models import AttributeEntity, Attribute


class AttributeEntityAdmin(admin.ModelAdmin):
    search_fields = ('uri', )
    readonly_fields = ('uri', 'path')


admin.site.register(AttributeEntity, AttributeEntityAdmin)
admin.site.register(Attribute, AttributeEntityAdmin)
