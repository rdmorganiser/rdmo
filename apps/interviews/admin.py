from django.contrib import admin

from .models import *


class InterviewAdmin(admin.ModelAdmin):
    list_display = ('project', 'title')
    list_display_links = ('title', )


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('project_title', 'interview_title', 'section_slug', 'subsection_slug', 'group_slug', 'question_slug')
    list_display_links = ('question_slug', )


admin.site.register(Interview, InterviewAdmin)
admin.site.register(Answer, AnswerAdmin)
