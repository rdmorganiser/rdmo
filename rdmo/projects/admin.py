from django import forms
from django.contrib import admin
from django.db.models import Prefetch
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .models import (
    Continuation,
    Integration,
    IntegrationOption,
    Invite,
    Issue,
    IssueResource,
    Membership,
    Project,
    Snapshot,
    Value,
    Visibility,
)
from .validators import ProjectParentValidator


class ProjectAdminForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = [
            'parent',
            'site',
            'title',
            'description',
            'catalog',
            'views'
        ]


    def clean(self):
        super().clean()
        ProjectParentValidator(self.instance)(self.cleaned_data)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm

    search_fields = ('title', 'user__username')
    list_display = ('title', 'owners', 'updated', 'created')
    readonly_fields = ('progress_count', 'progress_total')

    def get_queryset(self, request):
        return Project.objects.prefetch_related(
            Prefetch(
                'memberships',
                queryset=Membership.objects.filter(role='owner').select_related('user'),
                to_attr='owner_memberships'
            )
        )

    def owners(self, obj):
        return [membership.user.get_full_name() for membership in obj.owner_memberships]


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    search_fields = ('project__title', 'user__username', 'role')
    list_display = ('project', 'user', 'role')


@admin.register(Continuation)
class ContinuationAdmin(admin.ModelAdmin):
    search_fields = ('project__title', 'user__username')
    list_display = ('project', 'user', 'page')


@admin.register(Visibility)
class VisibilityAdmin(admin.ModelAdmin):
    search_fields = ('project__title', 'sites__domain', 'sites__name', 'groups__name')
    list_display = ('project', 'sites_list_display', 'groups_list_display')
    filter_horizontal = ('sites', 'groups')

    @admin.display(description=_('Sites'))
    def sites_list_display(self, obj):
        return _('all Sites') if obj.sites.count() == 0 else ', '.join([
            site.domain for site in obj.sites.all()
        ])

    @admin.display(description=_('Groups'))
    def groups_list_display(self, obj):
        return _('all Groups') if obj.groups.count() == 0 else ', '.join([
            group.name for group in obj.groups.all()
        ])


@admin.register(Integration)
class IntegrationAdmin(admin.ModelAdmin):
    search_fields = ('project__title', 'provider_key')
    list_display = ('project', 'provider_key')


@admin.register(IntegrationOption)
class IntegrationOptionAdmin(admin.ModelAdmin):
    search_fields = ('integration__project__title', 'key', 'value')
    list_display = ('integration', 'key', 'value')


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    search_fields = ('project__title', 'user__username', 'email', 'role')
    list_display = ('project', 'user', 'email', 'token', 'timestamp')
    readonly_fields = ('token', 'timestamp')


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    search_fields = ('project__title', 'task__uri', 'status')
    list_display = ('project', 'task', 'status')
    list_filter = ('status', )


@admin.register(IssueResource)
class IssueResourceAdmin(admin.ModelAdmin):
    search_fields = ('issue__project__title', 'url')
    list_display = ('issue', 'url')


@admin.register(Snapshot)
class SnapshotAdmin(admin.ModelAdmin):
    search_fields = ('title', 'project__title', 'project__user__username')
    list_display = ('title', 'project_title', 'project_owners', 'updated', 'created')

    def get_queryset(self, request):
        return Snapshot.objects.prefetch_related(
            Prefetch(
                'project__memberships',
                queryset=Membership.objects.filter(role='owner').select_related('user'),
                to_attr='owner_memberships'
            )
        ).select_related('project')

    def project_title(self, obj):
        url = reverse('admin:projects_project_change', args=[obj.project.id])
        link = f'<a href="{url}">{obj.project.title}</a>'
        return mark_safe(link)

    def project_owners(self, obj):
        return [membership.user.get_full_name() for membership in obj.project.owner_memberships]


@admin.register(Value)
class ValueAdmin(admin.ModelAdmin):
    search_fields = ('attribute__uri', 'project__title', 'snapshot__title', 'project__user__username')
    list_display = ('attribute', 'set_prefix', 'set_index', 'collection_index', 'set_collection', 'value_type',
                    'project_title', 'project_owners', 'snapshot_title', 'updated', 'created')
    list_filter = ('value_type', )

    def get_queryset(self, request):
        return Value.objects.prefetch_related(
            Prefetch(
                'project__memberships',
                queryset=Membership.objects.filter(role='owner').select_related('user'),
                to_attr='owner_memberships'
            )
        ).select_related('attribute', 'project', 'snapshot')

    def snapshot_title(self, obj):
        if obj.snapshot:
            return obj.snapshot.title

    def project_title(self, obj):
        url = reverse('admin:projects_project_change', args=[obj.project.id])
        link = f'<a href="{url}">{obj.project.title}</a>'
        return mark_safe(link)

    def project_owners(self, obj):
        return [membership.user.get_full_name() for membership in obj.project.owner_memberships]
