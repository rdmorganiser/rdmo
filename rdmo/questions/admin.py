from django import forms
from django.contrib import admin
from django.db import models

from rdmo.core.admin import ElementAdminForm
from rdmo.core.utils import get_language_fields

from .models import (
    Catalog,
    CatalogSection,
    Page,
    PageQuestion,
    PageQuestionSet,
    Question,
    QuestionSet,
    QuestionSetQuestion,
    QuestionSetQuestionSet,
    Section,
    SectionPage,
)
from .utils import get_widget_type_choices
from .validators import (
    CatalogLockedValidator,
    CatalogUniqueURIValidator,
    PageLockedValidator,
    PageUniqueURIValidator,
    QuestionLockedValidator,
    QuestionSetLockedValidator,
    QuestionSetQuestionSetValidator,
    QuestionSetUniqueURIValidator,
    QuestionUniqueURIValidator,
    SectionLockedValidator,
    SectionUniqueURIValidator,
)


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


class QuestionSetAdminForm(ElementAdminForm):

    class Meta:
        model = QuestionSet
        fields = '__all__'

    def clean(self):
        QuestionSetUniqueURIValidator(self.instance)(self.cleaned_data)
        QuestionSetQuestionSetValidator(self.instance)(self.cleaned_data)
        QuestionSetLockedValidator(self.instance)(self.cleaned_data)


class QuestionAdminForm(ElementAdminForm):
    widget_type = forms.ChoiceField(choices=get_widget_type_choices())

    class Meta:
        model = Question
        fields = '__all__'

    def clean(self):
        QuestionUniqueURIValidator(self.instance)(self.cleaned_data)
        QuestionLockedValidator(self.instance)(self.cleaned_data)


class CatalogSectionInline(admin.TabularInline):
    model = CatalogSection
    extra = 0


class CatalogAdmin(admin.ModelAdmin):
    form = CatalogAdminForm
    inlines = (CatalogSectionInline, )

    search_fields = ['uri', *get_language_fields('title')]
    list_display = ('uri', 'title', 'projects_count', 'available')
    readonly_fields = ('uri', )
    list_filter = ('available', )
    filter_horizontal = ('editors', 'sites', 'groups')

    def get_queryset(self, request):
        return super().get_queryset(request) \
                      .annotate(projects_count=models.Count('projects'))

    def projects_count(self, obj):
        return obj.projects_count


class SectionPageInline(admin.TabularInline):
    model = SectionPage
    extra = 0


class SectionAdmin(admin.ModelAdmin):
    form = SectionAdminForm
    inlines = (SectionPageInline, )

    search_fields = ['uri', *get_language_fields('title')]
    list_display = ('uri', 'title')
    readonly_fields = ('uri', )
    list_filter = ('catalogs', )
    filter_horizontal = ('editors', )


class PageQuestionSetInline(admin.TabularInline):
    model = PageQuestionSet
    extra = 0


class PageQuestionInline(admin.TabularInline):
    model = PageQuestion
    extra = 0


class PageAdmin(admin.ModelAdmin):
    form = PageAdminForm
    inlines = (PageQuestionSetInline, PageQuestionInline)

    search_fields = ['uri', *get_language_fields('title'), *get_language_fields('help')]
    list_display = ('uri', 'attribute', 'is_collection')
    readonly_fields = ('uri', )
    list_filter = ('sections__catalogs', 'sections', 'is_collection')
    filter_horizontal = ('editors', 'conditions')


class QuestionSetQuestionSetInline(admin.TabularInline):
    model = QuestionSetQuestionSet
    fk_name = 'parent'
    extra = 0


class QuestionSetQuestionInline(admin.TabularInline):
    model = QuestionSetQuestion
    extra = 0


class QuestionSetAdmin(admin.ModelAdmin):
    form = QuestionSetAdminForm
    inlines = (QuestionSetQuestionSetInline, QuestionSetQuestionInline)

    search_fields = ['uri', *get_language_fields('title'), *get_language_fields('help')]
    list_display = ('uri', 'attribute', 'is_collection')
    readonly_fields = ('uri', )
    list_filter = ('pages__sections__catalogs', 'pages__sections', 'pages', 'is_collection')
    filter_horizontal = ('editors', 'conditions')


class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm

    search_fields = ['uri', *get_language_fields('help'), *get_language_fields('text')]
    list_display = ('uri', 'attribute', 'text', 'is_collection')
    readonly_fields = ('uri', )
    list_filter = ('pages__sections__catalogs', 'pages__sections', 'pages', 'is_collection',
                   'widget_type', 'value_type')
    filter_horizontal = ('editors', 'optionsets', 'conditions')


admin.site.register(Catalog, CatalogAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(QuestionSet, QuestionSetAdmin)
admin.site.register(Question, QuestionAdmin)
