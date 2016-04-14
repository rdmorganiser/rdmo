from django.contrib import admin

from .models import *


class CatalogAdmin(admin.ModelAdmin):
    pass


class SectionAdmin(admin.ModelAdmin):
    pass


class SubsectionAdmin(admin.ModelAdmin):
    pass


class QuestionSetAdmin(admin.ModelAdmin):
    pass


class QuestionAdmin(admin.ModelAdmin):
    pass


class OptionAdmin(admin.ModelAdmin):
    pass


class ConditionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Catalog, CatalogAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Subsection, SubsectionAdmin)
admin.site.register(QuestionSet, QuestionSetAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(Condition, ConditionAdmin)
