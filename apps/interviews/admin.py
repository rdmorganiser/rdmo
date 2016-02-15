from django.contrib import admin

from .models import *


class InterviewAdmin(admin.ModelAdmin):
    list_display = ('project', 'title')
    list_display_links = ('title', )


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('interview', 'section_slug', 'subsection_slug', 'group_slug', 'question_slug', 'value')
    list_display_links = ('value', )

    # section_slug.short_description = 'Section'
    # subsection_slug.short_description = 'Subsection'
    # group_slug.short_description = 'Group'
    # question_slug.short_description = 'Question'


admin.site.register(Interview, InterviewAdmin)
admin.site.register(Answer, AnswerAdmin)
