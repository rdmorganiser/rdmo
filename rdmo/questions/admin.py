from django import forms
from django.contrib import admin
from django.db import models

from rdmo.core.admin import ElementAdminForm
from rdmo.core.utils import get_language_fields

from .models import Catalog, Page, Question, QuestionSet, Section
from .validators import (CatalogLockedValidator, CatalogUniqueURIValidator,
                         PageUniqueURIValidator, PageLockedValidator,
                         QuestionLockedValidator, QuestionSetLockedValidator,
                         QuestionSetUniqueURIValidator,
                         QuestionUniqueURIValidator, SectionLockedValidator,
                         SectionUniqueURIValidator, QuestionSetQuestionSetValidator)
from .utils import get_widget_type_choices


class CatalogAdminForm(ElementAdminForm):

    class Meta:
        model = Catalog
        fields = '__all__'

    def clean(self):
        CatalogUniqueURIValidator(self.instance)(self.cleaned_data)
        CatalogLockedValidator(self.instance)(self.cleaned_data)


class SectionAdminForm(ElementAdminForm):

    class Meta:
        model = Section
        fields = '__all__'

    def clean(self):
        SectionUniqueURIValidator(self.instance)(self.cleaned_data)
        SectionLockedValidator(self.instance)(self.cleaned_data)


class PageAdminForm(ElementAdminForm):

    class Meta:
        model = Page
        fields = '__all__'

    def clean(self):
        PageUniqueURIValidator(self.instance)(self.cleaned_data)
        PageLockedValidator(self.instance)(self.cleaned_data)


class QuestionSetAdminForm(forms.ModelForm):
    key = forms.SlugField(required=True)

    class Meta:
        model = QuestionSet
        fields = '__all__'

    def clean(self):
        QuestionSetUniqueURIValidator(self.instance)(self.cleaned_data)
        QuestionSetQuestionSetValidator(self.instance)(self.cleaned_data)
        QuestionSetLockedValidator(self.instance)(self.cleaned_data)


class QuestionAdminForm(forms.ModelForm):
    key = forms.SlugField(required=True)
    widget_type = forms.ChoiceField(choices=get_widget_type_choices())

    class Meta:
        model = Question
        fields = '__all__'

    def clean(self):
        QuestionUniqueURIValidator(self.instance)(self.cleaned_data)
        QuestionLockedValidator(self.instance)(self.cleaned_data)


class CatalogAdmin(admin.ModelAdmin):
    form = CatalogAdminForm

    search_fields = ['uri'] + get_language_fields('title')
    list_display = ('uri', 'title', 'projects_count', 'available')
    readonly_fields = ('uri', )
    list_filter = ('available', )

    def get_queryset(self, request):
        return super().get_queryset(request) \
                      .annotate(projects_count=models.Count('projects'))

    def projects_count(self, obj):
        return obj.projects_count


class SectionAdmin(admin.ModelAdmin):
    form = SectionAdminForm

    search_fields = ['uri'] + get_language_fields('title')
    list_display = ('uri', 'title')
    readonly_fields = ('uri', )
    list_filter = ('catalog', )


class PageAdmin(admin.ModelAdmin):
    form = PageAdminForm

    search_fields = ['uri'] + get_language_fields('title') + get_language_fields('help')
    list_display = ('uri', 'attribute', 'is_collection')
    readonly_fields = ('uri', )
    list_filter = ('section__catalog', 'section', 'is_collection')


class QuestionSetAdmin(admin.ModelAdmin):
    form = QuestionSetAdminForm

    search_fields = ['uri'] + get_language_fields('title') + get_language_fields('help')
    list_display = ('uri', 'attribute', 'is_collection')
    readonly_fields = ('uri', 'path')
    list_filter = ('page__section__catalog', 'page__section', 'is_collection')


class QuestionItemAdmin(admin.ModelAdmin):
    form = QuestionAdminForm

    search_fields = ['uri'] + get_language_fields('help') + get_language_fields('text')
    list_display = ('uri', 'attribute', 'text', 'is_collection')
    readonly_fields = ('uri', 'path')
    list_filter = ('page__section__catalog', 'page__section', 'is_collection', 'widget_type', 'value_type')


admin.site.register(Catalog, CatalogAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(QuestionSet, QuestionSetAdmin)
admin.site.register(Question, QuestionItemAdmin)
