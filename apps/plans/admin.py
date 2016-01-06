from django.contrib import admin

from .models import Plan, Template


class PlanAdmin(admin.ModelAdmin):
    pass


class TemplateAdmin(admin.ModelAdmin):
    pass

admin.site.register(Plan, PlanAdmin)
admin.site.register(Template, TemplateAdmin)
