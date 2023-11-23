from django.contrib import admin
from django.contrib.sites.models import Site
from django.db.models import Count, Value

from .models import AdditionalField, AdditionalFieldValue, ConsentFieldValue, Role


@admin.register(AdditionalField)
class AdditionalFieldAdmin(admin.ModelAdmin):
    pass


@admin.register(AdditionalFieldValue)
class AdditionalFieldValueAdmin(admin.ModelAdmin):
    readonly_fields = ('user', )


@admin.register(ConsentFieldValue)
class ConsentFieldValueAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'consent')

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    search_fields = ('user__username', 'user__email')
    list_filter = ('member', 'manager', 'editor', 'reviewer')

    list_display = ('user', 'email', 'members', 'managers', 'editors', 'reviewers')

    def get_queryset(self, request):
        return Role.objects.prefetch_related(
                'member', 'manager', 'editor', 'reviewer').annotate(
                    Count('member'), Count('manager'), Count('editor'), Count('reviewer'),
                    sites_count=Value(Site.objects.count())
                )

    @staticmethod
    def render_all_sites_or_join(obj, field_name: str) -> str:
        if getattr(obj, f'{field_name}__count', 0) == obj.sites_count:
            return 'all Sites'
        return ', '.join([site.domain for site in getattr(obj, field_name).all()])

    def email(self, obj):
        return obj.user.email

    def members(self, obj):
        return self.render_all_sites_or_join(obj, 'member')

    def managers(self, obj):
        return self.render_all_sites_or_join(obj, 'manager')

    def editors(self, obj):
        return self.render_all_sites_or_join(obj, 'editor')

    def reviewers(self, obj):
        return self.render_all_sites_or_join(obj, 'reviewer')
