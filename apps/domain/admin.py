from django.contrib import admin

from .models import AttributeEntity, Attribute, VerboseName, Range


class AttributeEntityAdmin(admin.ModelAdmin):
    readonly_fields = ('uri', 'label', 'parent_collection', 'is_attribute')


admin.site.register(AttributeEntity, AttributeEntityAdmin)
admin.site.register(Attribute, AttributeEntityAdmin)
admin.site.register(VerboseName)
admin.site.register(Range)
