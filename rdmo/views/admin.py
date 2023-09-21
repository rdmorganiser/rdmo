from django import forms
from django.contrib import admin

from rdmo.core.utils import get_language_fields

from .models import View
from .validators import ViewLockedValidator, ViewUniqueURIValidator


class ViewAdminForm(forms.ModelForm):
    uri_path = forms.SlugField(required=True)

    class Meta:
        model = View
        fields = '__all__'

    def clean(self):
        ViewUniqueURIValidator(self.instance)(self.cleaned_data)
        ViewLockedValidator(self.instance)(self.cleaned_data)


class ViewAdmin(admin.ModelAdmin):
    form = ViewAdminForm

    search_fields = ['uri', *get_language_fields('title'), *get_language_fields('help')]
    list_display = ('uri', 'title', 'help', 'available')
    readonly_fields = ('uri', )
    list_filter = ('available', )
    filter_horizontal = ('catalogs', 'sites', 'editors', 'groups')


admin.site.register(View, ViewAdmin)
