from django.contrib import admin

from .models import Catalog, Section, Subsection, QuestionSet, Question


class CatalogAdmin(admin.ModelAdmin):
    search_fields = ('uri', )
    readonly_fields = ('uri', )


class SectionAdmin(admin.ModelAdmin):
    search_fields = ('uri', )
    readonly_fields = ('uri', 'path')


class SubsectionAdmin(admin.ModelAdmin):
    search_fields = ('uri', )
    readonly_fields = ('uri', 'path')


class QuestionSetAdmin(admin.ModelAdmin):
    search_fields = ('uri', )
    readonly_fields = ('uri', 'path')
    list_display = ('uri', 'is_collection')


class QuestionItemAdmin(admin.ModelAdmin):
    search_fields = ('uri', )
    readonly_fields = ('uri', 'path')



admin.site.register(Catalog, CatalogAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Subsection, SubsectionAdmin)
admin.site.register(QuestionSet, QuestionSetAdmin)
admin.site.register(Question, QuestionItemAdmin)
