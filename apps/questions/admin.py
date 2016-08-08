from django.contrib import admin

from .models import *


class SectionAdmin(admin.ModelAdmin):
    readonly_fields = ('label_en', 'label_de')


class SubsectionAdmin(admin.ModelAdmin):
    readonly_fields = ('label_en', 'label_de')


class QuestionEntityAdmin(admin.ModelAdmin):
    readonly_fields = ('label_en', 'label_de')


class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ('label_en', 'label_de')


admin.site.register(Catalog)
admin.site.register(Section, SectionAdmin)
admin.site.register(Subsection, SubsectionAdmin)
admin.site.register(QuestionEntity, QuestionEntityAdmin)
admin.site.register(Question, QuestionAdmin)
