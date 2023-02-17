from django.contrib import admin
from django.contrib.sites.models import Site
from django.db.models import Count, Value

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
    list_filter = ('member', 'manager', 'editor', 'reviewer')

    list_display = ('user', 'member_at', 'member_at', 'manager_at', 'editor_at', 'reviewer_at')

    def get_queryset(self, request):
        return Role.objects.prefetch_related(
                'member', 'manager', 'editor', 'reviewer').annotate(
                    Count('member'), Count('manager'), Count('editor'), Count('reviewer'),
                    sites_count=Value(Site.objects.count())
                )

    def member_at(self, obj):
        if obj.member__count == obj.sites_count:
            return 'all sites'
        return ', '.join([site.domain for site in obj.member.all()])

    def manager_at(self, obj):
        if obj.manager__count == obj.sites_count:
            return 'all sites'
        return ', '.join([site.domain for site in obj.manager.all()])

    def editor_at(self, obj):
        if obj.editor__count == obj.sites_count:
            return 'all sites'
        return ', '.join([site.domain for site in obj.editor.all()])

    def reviewer_at(self, obj):
        if obj.reviewer__count == obj.sites_count:
            return 'all sites'
        return ', '.join([site.domain for site in obj.reviewer.all()])


admin.site.register(AdditionalField, AdditionalFieldAdmin)
admin.site.register(AdditionalFieldValue, AdditionalFieldValueAdmin)
admin.site.register(ConsentFieldValue, ConsentFieldValueAdmin)
admin.site.register(Role, RoleAdmin)
