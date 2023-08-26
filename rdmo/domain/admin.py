from django import forms
from django.contrib import admin
from django.db import models

from .models import Attribute
from .validators import AttributeLockedValidator, AttributeParentValidator, AttributeUniqueURIValidator


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

    list_display = ('uri', 'projects_count', 'values_count')
    search_fields = ('uri', )
    readonly_fields = ('uri', 'path', 'projects_count', 'values_count')
    filter_horizontal = ('editors', )

    def get_queryset(self, request):
        return super().get_queryset(request) \
                      .annotate(values_count=models.Count('values')) \
                      .annotate(projects_count=models.Count('values__project', distinct=True))

    def values_count(self, obj):
        return obj.values_count

    def projects_count(self, obj):
        return obj.projects_count


admin.site.register(Attribute, AttributeAdmin)
