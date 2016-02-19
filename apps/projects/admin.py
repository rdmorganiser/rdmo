from django.contrib import admin

from .models import *


class ProjectAdmin(admin.ModelAdmin):
    pass


class SnapshotAdmin(admin.ModelAdmin):
    pass


class ValueSetAdmin(admin.ModelAdmin):
    pass


class ValueAdmin(admin.ModelAdmin):
    pass

admin.site.register(Project, ProjectAdmin)
admin.site.register(Snapshot, SnapshotAdmin)
admin.site.register(ValueSet, ValueSetAdmin)
admin.site.register(Value, ValueAdmin)
