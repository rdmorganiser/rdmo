from django import forms
from django.contrib import admin
from django.contrib.sites.admin import SiteAdmin as DjangoSiteAdmin
from django.contrib.sites.models import Site


class ElementAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['uri_path'].required = True

# the original Django SiteAdmin needs to be unregistered first
if admin.site.is_registered(Site):
    admin.site.unregister(Site)


@admin.register(Site)
class SiteAdmin(DjangoSiteAdmin):
    list_display = ('id', 'domain', 'name')
    list_display_links = ('domain',)
    search_fields = ('id', 'domain', 'name')
    ordering = ('id',)
