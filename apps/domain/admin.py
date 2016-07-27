from django.contrib import admin

from .models import *


class AttributeEntityAdmin(admin.ModelAdmin):

    readonly_fields = ('full_title', 'parent_collection')

admin.site.register(AttributeEntity, AttributeEntityAdmin)
admin.site.register(Attribute, AttributeEntityAdmin)
admin.site.register(Option)
admin.site.register(Range)
