from django.contrib import admin

from .models import DetailKey, Profile


class DetailKeyAdmin(admin.ModelAdmin):
    pass


class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('user', )

admin.site.register(DetailKey, DetailKeyAdmin)
admin.site.register(Profile, ProfileAdmin)
