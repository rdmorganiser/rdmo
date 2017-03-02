from django.contrib import admin

from .models import Condition


class ConditionAdmin(admin.ModelAdmin):
    search_fields = ('uri', )
    readonly_fields = ('uri', )


admin.site.register(Condition, ConditionAdmin)
