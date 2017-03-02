from django.contrib import admin

from .models import View


class ViewAdmin(admin.ModelAdmin):
    readonly_fields = ('uri', )

admin.site.register(View, ViewAdmin)
