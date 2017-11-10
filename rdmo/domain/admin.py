from django.contrib import admin

from .models import AttributeEntity, Attribute, VerboseName, Range


class AttributeEntityAdmin(admin.ModelAdmin):
    search_fields = ('uri', )
    readonly_fields = ('uri', 'path', 'parent_collection', 'is_attribute')


class RangeAdmin(admin.ModelAdmin):
    search_fields = ('attribute__uri', )


class VerboseNameAdmin(admin.ModelAdmin):
    search_fields = ('attribute_entity__uri', )


admin.site.register(AttributeEntity, AttributeEntityAdmin)
admin.site.register(Attribute, AttributeEntityAdmin)
admin.site.register(Range, RangeAdmin)
admin.site.register(VerboseName, VerboseNameAdmin)
