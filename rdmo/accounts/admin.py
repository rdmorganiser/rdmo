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

    readonly_fields = ('user', )

    def get_queryset(self, request):
        return Role.objects.prefetch_related(
                'member', 'manager', 'editor', 'reviewer').annotate(
                    Count('member', distinct=True),
                    Count('manager', distinct=True),
                    Count('editor', distinct=True),
                    Count('reviewer', distinct=True),
                    sites_count=Value(Site.objects.count())
                )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['member'].widget.can_add_related = False
        form.base_fields['manager'].widget.can_add_related = False
        form.base_fields['editor'].widget.can_add_related = False
        form.base_fields['reviewer'].widget.can_add_related = False

        return form

    @staticmethod
    def get_sites_for_role(obj, field_name: str) -> str:
        if getattr(obj, f'{field_name}__count', 0) == obj.sites_count:
            return 'all Sites'
        return ', '.join([site.domain for site in getattr(obj, field_name).all()])

    def email(self, obj):
        return obj.user.email

    def members(self, obj):
        return self.get_sites_for_role(obj, 'member')

    def managers(self, obj):
        return self.get_sites_for_role(obj, 'manager')

    def editors(self, obj):
        return self.get_sites_for_role(obj, 'editor')

    def reviewers(self, obj):
        return self.get_sites_for_role(obj, 'reviewer')
