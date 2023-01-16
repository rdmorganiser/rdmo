from django import forms
from django.contrib import admin

from rdmo.core.admin import ElementAdminForm
from rdmo.core.utils import get_language_fields

from .models import Option, OptionSet
from .validators import (OptionLockedValidator, OptionSetLockedValidator,
                         OptionSetUniqueURIValidator, OptionUniqueURIValidator)


class OptionSetAdminForm(ElementAdminForm):

    class Meta:
        model = OptionSet
        fields = '__all__'

    def clean(self):
        OptionSetUniqueURIValidator(self.instance)(self.cleaned_data)
        OptionSetLockedValidator(self.instance)(self.cleaned_data)


class OptionAdminForm(ElementAdminForm):

    class Meta:
        model = Option
        fields = '__all__'

    def clean(self):
        OptionUniqueURIValidator(self.instance)(self.cleaned_data)
        OptionLockedValidator(self.instance)(self.cleaned_data)


class OptionSetAdmin(admin.ModelAdmin):
    form = OptionSetAdminForm

    search_fields = ('uri', )
    list_display = ('uri', )
    readonly_fields = ('uri', )


class OptionAdmin(admin.ModelAdmin):
    form = OptionAdminForm

    search_fields = ['uri'] + get_language_fields('text')
    list_display = ('uri', 'text', 'additional_input')
    readonly_fields = ('uri', )
    list_filter = ('optionsets', 'additional_input')


admin.site.register(OptionSet, OptionSetAdmin)
admin.site.register(Option, OptionAdmin)
