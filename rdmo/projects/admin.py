from django.contrib import admin

from .models import Project, Membership, Snapshot, Value


class ProjectAdmin(admin.ModelAdmin):
    search_fields = ('title', 'user__username')
    list_display = ('title', 'owners')

    def owners(self, obj):
        return ', '.join([user.username for user in obj.owners])


class MembershipAdmin(admin.ModelAdmin):
    search_fields = ('project__title', 'user__username', 'role')
    list_display = ('project', 'user', 'role')


class SnapshotAdmin(admin.ModelAdmin):
    search_fields = ('title', 'project__title', 'project__user__username')
    list_display = ('title', 'project')


class ValueAdmin(admin.ModelAdmin):
    search_fields = ('attribute__uri', 'project__title', 'snapshot__title', 'project__user__username')
    list_display = ('attribute', 'set_index', 'collection_index', 'project', 'snapshot_title')
    list_filter = ('value_type', )

    def snapshot_title(self, obj):
        if obj.snapshot:
            return obj.snapshot.title


admin.site.register(Project, ProjectAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Snapshot, SnapshotAdmin)
admin.site.register(Value, ValueAdmin)
