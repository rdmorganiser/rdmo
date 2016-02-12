from django.contrib import admin

from .models import *


class InterviewAdmin(admin.ModelAdmin):
    list_display = ('project', 'title')
    list_display_links = ('title', )


class SectionAdmin(admin.ModelAdmin):
    list_display = ('section_slug', 'title')
    list_display_links = ('title', )

    def section_slug(self, obj):
        return obj.slug

    section_slug.short_description = 'Section'


class SubsectionAdmin(admin.ModelAdmin):
    list_display = ('section_slug', 'subsection_slug', 'title')
    list_display_links = ('title', )

    def section_slug(self, obj):
        return obj.section.slug

    section_slug.short_description = 'Section'

    def subsection_slug(self, obj):
        return obj.slug

    subsection_slug.short_description = 'Subsection'


class GroupAdmin(admin.ModelAdmin):
    list_display = ('section_slug', 'subsection_slug', 'group_slug', 'title')
    list_display_links = ('title', )

    def section_slug(self, obj):
        return obj.subsection.section.slug

    section_slug.short_description = 'Section'

    def subsection_slug(self, obj):
        return obj.subsection.slug

    subsection_slug.short_description = 'Subsection'

    def group_slug(self, obj):
        return obj.slug

    group_slug.short_description = 'Group'


# class JumpAdmin(admin.ModelAdmin):
#     pass


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('section_slug', 'subsection_slug', 'group_slug', 'question_slug', 'text')
    list_display_links = ('text', )

    def section_slug(self, obj):
        return obj.group.subsection.section.slug

    section_slug.short_description = 'Section'

    def subsection_slug(self, obj):
        return obj.group.subsection.slug

    subsection_slug.short_description = 'Subsection'

    def group_slug(self, obj):
        return obj.group.slug

    group_slug.short_description = 'Group'

    def question_slug(self, obj):
        return obj.slug

    question_slug.short_description = 'Question'


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('interview', 'section_slug', 'subsection_slug', 'group_slug', 'question_slug', 'value')
    list_display_links = ('value', )

    def section_slug(self, obj):
        return obj.question.group.subsection.section.slug

    section_slug.short_description = 'Section'

    def subsection_slug(self, obj):
        return obj.question.group.subsection.slug

    subsection_slug.short_description = 'Subsection'

    def group_slug(self, obj):
        return obj.question.group.slug

    group_slug.short_description = 'Group'

    def question_slug(self, obj):
        return obj.question.slug

    question_slug.short_description = 'Question'


admin.site.register(Interview, InterviewAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Subsection, SubsectionAdmin)
admin.site.register(Group, GroupAdmin)
#admin.site.register(Jump, JumpAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
