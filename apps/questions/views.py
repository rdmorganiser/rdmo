from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from apps.core.views import ProtectedCreateView, ProtectedUpdateView, ProtectedDeleteView

from .models import *


class QuestionViewMixin():
    def get_success_url(self):
        return reverse('questions')


def questions(request):
    catalog = Catalog.objects.first()
    return render(request, 'questions/questions.html', {'catalog': catalog})


def questions_sequence_gv(request):
    content = render_to_string('questions/questions_sequence.gv', {
        'sections': Section.objects.all(),
        'question_ids': [question.pk for question in Question.objects.all()]
    })

    # remove empty lines
    # content = "".join([s for s in content.strip().splitlines(True) if s.strip()])

    return HttpResponse(content, content_type='text/plain')


class CatalogCreateView(QuestionViewMixin, ProtectedCreateView):
    model = Catalog
    fields = '__all__'


class CatalogUpdateView(QuestionViewMixin, ProtectedUpdateView):
    model = Catalog
    fields = '__all__'


class CatalogDeleteView(QuestionViewMixin, ProtectedDeleteView):
    model = Catalog


class CatalogCreateSectionView(QuestionViewMixin, ProtectedCreateView):
    model = Section
    fields = ['title_en', 'title_de']

    def dispatch(self, *args, **kwargs):
        self.catalog = get_object_or_404(Catalog, pk=self.kwargs['pk'])
        return super(CatalogCreateSectionView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.catalog = self.catalog
        return super(SubsectionCreateSubsectionView, self).form_valid(form)


class SectionCreateView(QuestionViewMixin, ProtectedCreateView):
    model = Section
    fields = '__all__'


class SectionUpdateView(QuestionViewMixin, ProtectedUpdateView):
    model = Section
    fields = '__all__'


class SectionDeleteView(QuestionViewMixin, ProtectedDeleteView):
    model = Section


class SubsectionCreateSubsectionView(QuestionViewMixin, ProtectedCreateView):
    model = Subsection
    fields = ('order', 'title_en', 'title_de')

    def dispatch(self, *args, **kwargs):
        self.section = get_object_or_404(Section, pk=self.kwargs['pk'])
        return super(SubsectionCreateSubsectionView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.section = self.section
        return super(SubsectionCreateSubsectionView, self).form_valid(form)


class SubsectionCreateView(QuestionViewMixin, ProtectedCreateView):
    model = Subsection
    fields = '__all__'


class SubsectionUpdateView(QuestionViewMixin, ProtectedUpdateView):
    model = Subsection
    fields = '__all__'


class SubsectionDeleteView(QuestionViewMixin, ProtectedDeleteView):
    model = Subsection


class SubsectionCreateQuestionView(QuestionViewMixin, ProtectedCreateView):
    model = Question
    fields = ['order', 'text_en', 'text_de', 'widget_type']

    def dispatch(self, *args, **kwargs):
        self.subsection = get_object_or_404(Subsection, pk=self.kwargs['pk'])
        return super(SubsectionCreateQuestionView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.subsection = self.subsection
        return super(SubsectionCreateQuestionView, self).form_valid(form)


class SubsectionCreateQuestionSetView(QuestionViewMixin, ProtectedCreateView):
    model = QuestionSet
    fields = ['order']

    def dispatch(self, *args, **kwargs):
        self.subsection = get_object_or_404(Subsection, pk=self.kwargs['pk'])
        return super(SubsectionCreateQuestionSetView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.subsection = self.subsection
        return super(SubsectionCreateQuestionSetView, self).form_valid(form)


class QuestionCreateView(QuestionViewMixin, ProtectedCreateView):
    model = Question
    fields = '__all__'


class QuestionUpdateView(QuestionViewMixin, ProtectedUpdateView):
    model = Question
    fields = '__all__'


class QuestionDeleteView(QuestionViewMixin, ProtectedDeleteView):
    model = Question


class QuestionSetCreateView(QuestionViewMixin, ProtectedCreateView):
    model = QuestionSet
    fields = '__all__'


class QuestionSetUpdateView(QuestionViewMixin, ProtectedUpdateView):
    model = QuestionSet
    fields = '__all__'


class QuestionSetDeleteView(QuestionViewMixin, ProtectedDeleteView):
    model = QuestionSet


class QuestionSetCreateQuestionView(QuestionViewMixin, ProtectedCreateView):
    model = Question
    fields = ['order', 'text_en', 'text_de', 'widget_type']

    def dispatch(self, *args, **kwargs):
        self.questionset = get_object_or_404(QuestionSet, pk=self.kwargs['pk'])
        return super(QuestionSetCreateQuestionView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.subsection = self.questionset.subsection
        form.instance.questionset = self.questionset
        return super(QuestionSetCreateQuestionView, self).form_valid(form)
