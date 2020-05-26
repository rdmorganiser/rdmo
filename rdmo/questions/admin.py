from django.contrib import admin

from rdmo.core.utils import get_language_fields

from .models import Catalog, Section, QuestionSet, Question


class CatalogAdmin(admin.ModelAdmin):
    search_fields = ['uri'] + get_language_fields('title')
    list_display = ('uri', 'title')
    readonly_fields = ('uri', )


class SectionAdmin(admin.ModelAdmin):
    search_fields = ['uri'] + get_language_fields('title')
    list_display = ('uri', 'title')
    readonly_fields = ('uri', 'path')
    list_filter = ('catalog', )


class QuestionSetAdmin(admin.ModelAdmin):
    search_fields = ['uri'] + get_language_fields('title') + get_language_fields('help')
    list_display = ('uri', 'attribute', 'is_collection')
    readonly_fields = ('uri', 'path')
    list_filter = ('section__catalog', 'section', 'is_collection')


class QuestionItemAdmin(admin.ModelAdmin):
    search_fields = ['uri'] + get_language_fields('help') + get_language_fields('text')
    list_display = ('uri', 'attribute', 'text', 'is_collection')
    readonly_fields = ('uri', 'path')
    list_filter = ('questionset__section__catalog', 'questionset__section', 'is_collection', 'widget_type', 'value_type')


admin.site.register(Catalog, CatalogAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(QuestionSet, QuestionSetAdmin)
admin.site.register(Question, QuestionItemAdmin)
