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
    search_fields = ('user__username', 'user__email')
    list_filter = ('member', 'manager', 'editor')
    list_display = ('user', 'manager_str', 'editor_str', 'member_str')

    def member_str(self, obj):
        return ', '.join([site.name for site in obj.member.all()])
    def manager_str(self, obj):
        return ', '.join([site.name for site in obj.manager.all()])
    def editor_str(self, obj):
        if obj.instance_editor:
            return "Instance Editor"
        return ', '.join([site.name for site in obj.editor.all()])


admin.site.register(AdditionalField, AdditionalFieldAdmin)
admin.site.register(AdditionalFieldValue, AdditionalFieldValueAdmin)
admin.site.register(ConsentFieldValue, ConsentFieldValueAdmin)
admin.site.register(Role, RoleAdmin)
