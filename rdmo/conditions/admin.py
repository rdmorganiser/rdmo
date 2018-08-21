from django.contrib import admin

from .models import Condition


class ConditionAdmin(admin.ModelAdmin):
    search_fields = ('uri', 'source', 'text_de')
    list_display = ('uri', 'source', 'relation', 'target_text', 'target_option')
    readonly_fields = ('uri', )
    list_filter = ('relation', )

admin.site.register(Condition, ConditionAdmin)
