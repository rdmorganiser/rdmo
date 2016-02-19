from django.contrib import admin

from .models import *


class CatalogAdmin(admin.ModelAdmin):
    pass


class SectionAdmin(admin.ModelAdmin):
    pass
    # list_display = ('slug', 'title')
    # list_display_links = ('title', )


class SubsectionAdmin(admin.ModelAdmin):
    pass
    # list_display = ('section_slug', 'slug', 'title')
    # list_display_links = ('title', )


class QuestionSetAdmin(admin.ModelAdmin):
    pass
    # list_display = ('section_slug', 'subsection_slug', 'group_slug', 'slug', 'text')
    # list_display_links = ('text', )


class QuestionAdmin(admin.ModelAdmin):
    pass
    # list_display = ('section_slug', 'subsection_slug', 'slug', 'text')
    # list_display_links = ('text', )


class ConditionAdmin(admin.ModelAdmin):
    pass
    # list_display = ('section_slug', 'subsection_slug', 'group_title')
    # list_display_links = ('group_title', )


admin.site.register(Catalog, CatalogAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Subsection, SubsectionAdmin)
admin.site.register(QuestionSet, QuestionSetAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Condition, ConditionAdmin)
