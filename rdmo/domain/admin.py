from django import forms
from django.contrib import admin

from .models import Attribute
from .validators import (AttributeLockedValidator, AttributeParentValidator,
                         AttributeUniqueURIValidator)


class AttributeAdminForm(forms.ModelForm):
    key = forms.SlugField(required=True)

    class Meta:
        model = Attribute
        fields = '__all__'

    def clean(self):
        AttributeUniqueURIValidator(self.instance)(self.cleaned_data)
        AttributeParentValidator(self.instance)(self.cleaned_data)
        AttributeLockedValidator(self.instance)(self.cleaned_data)


class AttributeAdmin(admin.ModelAdmin):
    form = AttributeAdminForm

    list_display = ('uri', 'projects_count', 'values_count', 'locked')
    search_fields = ('uri', )
    readonly_fields = ('uri', 'path')


admin.site.register(Attribute, AttributeAdmin)
