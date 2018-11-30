from django.contrib import admin

from .models import Catalog, Section, QuestionSet, Question


class CatalogAdmin(admin.ModelAdmin):
    search_fields = ('uri', 'title_en', 'title_de')
    list_display = ('uri', 'title')
    readonly_fields = ('uri', )


class SectionAdmin(admin.ModelAdmin):
    search_fields = ('uri', 'title_en', 'title_de')
    list_display = ('uri', 'title')
    readonly_fields = ('uri', 'path')


class QuestionSetAdmin(admin.ModelAdmin):
    search_fields = ('uri', 'help_en', 'help_de')
    list_display = ('uri', 'attribute', 'is_collection')
    readonly_fields = ('uri', 'path')
    list_filter = ('is_collection', )


class QuestionItemAdmin(admin.ModelAdmin):
    search_fields = ('uri', 'text_en', 'text_de', 'help_en', 'help_de')
    list_display = ('uri', 'attribute', 'text', 'is_collection')
    readonly_fields = ('uri', 'path')
    list_filter = ('is_collection', 'widget_type', 'value_type')



admin.site.register(Catalog, CatalogAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(QuestionSet, QuestionSetAdmin)
admin.site.register(Question, QuestionItemAdmin)
