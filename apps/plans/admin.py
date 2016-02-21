from django.contrib import admin

from .models import Attribute, AttributeSet, Template


class AttributeAdmin(admin.ModelAdmin):
    pass


class AttributeSetAdmin(admin.ModelAdmin):
    pass


class TemplateAdmin(admin.ModelAdmin):
    pass

admin.site.register(Attribute, AttributeAdmin)
admin.site.register(AttributeSet, AttributeSetAdmin)
admin.site.register(Template, TemplateAdmin)
