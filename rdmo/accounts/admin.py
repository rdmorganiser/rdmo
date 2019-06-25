from django.contrib import admin

from .models import AdditionalField, AdditionalFieldValue, ConsentFieldValue, Role


class AdditionalFieldAdmin(admin.ModelAdmin):
    pass


class AdditionalFieldValueAdmin(admin.ModelAdmin):
    readonly_fields = ('user', )


class ConsentFieldValueAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'consent')

    def has_add_permission(self, request, obj=None):
        return False


class RoleAdmin(admin.ModelAdmin):
    pass


admin.site.register(AdditionalField, AdditionalFieldAdmin)
admin.site.register(AdditionalFieldValue, AdditionalFieldValueAdmin)
admin.site.register(ConsentFieldValue, ConsentFieldValueAdmin)
admin.site.register(Role, RoleAdmin)
