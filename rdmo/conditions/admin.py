from django import forms
from django.contrib import admin

from .models import Condition
from .validators import ConditionLockedValidator, ConditionUniqueURIValidator


class ConditionAdminForm(forms.ModelForm):
    key = forms.SlugField(required=True)

    class Meta:
        model = Condition
        fields = '__all__'

    def clean(self):
        ConditionUniqueURIValidator(self.instance)(self.cleaned_data)
        ConditionLockedValidator(self.instance)(self.cleaned_data)


class ConditionAdmin(admin.ModelAdmin):
    form = ConditionAdminForm

    search_fields = ('uri', 'source__uri')
    list_display = ('uri', 'source', 'relation', 'target_text', 'target_option')
    readonly_fields = ('uri', )
    list_filter = ('relation', )
    filter_horizontal = ('editors', )


admin.site.register(Condition, ConditionAdmin)
