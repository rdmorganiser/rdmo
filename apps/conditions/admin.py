from django.contrib import admin

from .models import Condition


class ConditionAdmin(admin.ModelAdmin):
    readonly_fields = ('uri', )


admin.site.register(Condition, ConditionAdmin)
