from django.contrib import admin

from .models import Interview, Topic, Category, Jump, Question, Answer


class InterviewAdmin(admin.ModelAdmin):
    list_display = ('project', 'title')
    list_display_links = ('title', )


class TopicAdmin(admin.ModelAdmin):
    list_display = ('topic_slug', 'title')
    list_display_links = ('title', )

    def topic_slug(self, obj):
        return obj.slug

    topic_slug.short_description = 'Topic'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('topic_slug', 'category_slug', 'title')
    list_display_links = ('title', )

    def topic_slug(self, obj):
        return obj.topic.slug

    topic_slug.short_description = 'Topic'

    def category_slug(self, obj):
        return obj.slug

    category_slug.short_description = 'Category'

class JumpAdmin(admin.ModelAdmin):
    pass


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('topic_slug', 'category_slug', 'question_slug', 'text')
    list_display_links = ('text', )

    def topic_slug(self, obj):
        return obj.category.topic.slug

    topic_slug.short_description = 'Topic'

    def category_slug(self, obj):
        return obj.category.slug

    category_slug.short_description = 'Category'

    def question_slug(self, obj):
        return obj.slug

    question_slug.short_description = 'Question'


class AnswerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Interview, InterviewAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Jump, JumpAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
