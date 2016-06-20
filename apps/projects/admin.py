from django.contrib import admin

from .models import *


admin.site.register(Project)
admin.site.register(Snapshot)
admin.site.register(Value)
