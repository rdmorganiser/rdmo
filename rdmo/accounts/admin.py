from django.contrib import admin

from .models import AdditionalField, AdditionalFieldValue, ConsentFieldValue


class AdditionalFieldAdmin(admin.ModelAdmin):
    pass


class AdditionalFieldValueAdmin(admin.ModelAdmin):
    readonly_fields = ('user', )


class ConsentFieldValueAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'consent')


admin.site.register(AdditionalField, AdditionalFieldAdmin)
admin.site.register(AdditionalFieldValue, AdditionalFieldValueAdmin)
admin.site.register(ConsentFieldValue, ConsentFieldValueAdmin)
