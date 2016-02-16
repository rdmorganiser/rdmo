from django.contrib import admin

from .models import *


class SectionAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title')
    list_display_links = ('title', )

    # section_slug.short_description = 'Section'


class SubsectionAdmin(admin.ModelAdmin):
    list_display = ('section_slug', 'slug', 'title')
    list_display_links = ('title', )

    # subsection_slug.short_description = 'Subsection'


class GroupAdmin(admin.ModelAdmin):
    list_display = ('section_slug', 'subsection_slug', 'slug', 'title')
    list_display_links = ('title', )

    # section_slug.short_description = 'Section'
    # subsection_slug.short_description = 'Subsection'
    # group_slug.short_description = 'Group'


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('section_slug', 'subsection_slug', 'group_slug', 'slug', 'text')
    list_display_links = ('text', )

    # section_slug.short_description = 'Section'
    # subsection_slug.short_description = 'Subsection'
    # group_slug.short_description = 'Group'
    # question_slug.short_description = 'Question'


class ConditionAdmin(admin.ModelAdmin):
    pass

    # list_display = ('section_slug', 'subsection_slug', 'group_slug', 'slug', 'text')
    # list_display_links = ('text', )

admin.site.register(Section, SectionAdmin)
admin.site.register(Subsection, SubsectionAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Condition, ConditionAdmin)
