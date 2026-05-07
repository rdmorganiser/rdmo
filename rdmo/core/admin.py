from django import forms
from django.contrib import admin
from django.contrib.sites.admin import SiteAdmin
from django.contrib.sites.models import Site


class ElementAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['uri_path'].required = True


if admin.site.is_registered(Site):
    admin.site.unregister(Site)


@admin.register(Site)
class CustomSiteAdmin(SiteAdmin):
    list_display = ('id', 'domain', 'name')
    search_fields = ('domain', 'name')
