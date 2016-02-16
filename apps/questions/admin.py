from django.contrib import admin

from .models import *


class SectionAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title')
    list_display_links = ('title', )


class SubsectionAdmin(admin.ModelAdmin):
    list_display = ('section_slug', 'slug', 'title')
    list_display_links = ('title', )


class GroupAdmin(admin.ModelAdmin):
    list_display = ('section_slug', 'subsection_slug', 'slug', 'title')
    list_display_links = ('title', )


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('section_slug', 'subsection_slug', 'group_slug', 'slug', 'text')
    list_display_links = ('text', )


class ConditionAdmin(admin.ModelAdmin):
    list_display = ('section_slug', 'subsection_slug', 'group_slug', 'group_title')
    list_display_links = ('group_title', )


admin.site.register(Section, SectionAdmin)
admin.site.register(Subsection, SubsectionAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Condition, ConditionAdmin)
