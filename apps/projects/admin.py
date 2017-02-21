from django.contrib import admin

from .models import Project, Membership, Snapshot, Value


admin.site.register(Project)
admin.site.register(Membership)
admin.site.register(Snapshot)
admin.site.register(Value)
