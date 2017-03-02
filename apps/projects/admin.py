from django.contrib import admin

from .models import Project, Snapshot, Value


admin.site.register(Project)
admin.site.register(Snapshot)
admin.site.register(Value)
