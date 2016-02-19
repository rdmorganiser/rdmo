from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from apps.core.views import ProtectedCreateView, ProtectedUpdateView, ProtectedDeleteView

from .models import *


def catalogs(request):
    return render(request, 'catalogs/catalogs.html', {'catalogs': Catalog.objects.all()})


def catalog(request, pk):
    catalog = get_object_or_404(Catalog, pk=pk)
    return render(request, 'catalogs/catalog.html', {'catalog': catalog})


class CatalogCreateView(ProtectedCreateView):
    model = Catalog
    fields = '__all__'


class CatalogUpdateView(ProtectedUpdateView):
    model = Catalog
    fields = '__all__'


class CatalogDeleteView(ProtectedDeleteView):
    model = Catalog
    success_url = reverse_lazy('catalogs')


class CatalogCreateSectionView(ProtectedCreateView):
    model = Section
    fields = ['title_en', 'title_de']

    def dispatch(self, *args, **kwargs):
        self.catalog = get_object_or_404(Catalog, pk=self.kwargs['pk'])
        return super(CatalogCreateSectionView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.catalog = self.catalog
        return super(CatalogCreateSectionView, self).form_valid(form)

    def get_success_url(self):
        return reverse('catalog', kwargs={'pk': self.object.catalog.pk})


class SectionCreateView(ProtectedCreateView):
    model = Section
    fields = '__all__'


class SectionUpdateView(ProtectedUpdateView):
    model = Section
    fields = '__all__'


class SectionDeleteView(ProtectedDeleteView):
    model = Section


class SubsectionCreateSubsectionView(ProtectedCreateView):
    model = Subsection
    fields = ('order', 'title_en', 'title_de')

    def dispatch(self, *args, **kwargs):
        self.section = get_object_or_404(Section, pk=self.kwargs['pk'])
        return super(SubsectionCreateSubsectionView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.section = self.section
        return super(SubsectionCreateSubsectionView, self).form_valid(form)


class SubsectionCreateView(ProtectedCreateView):
    model = Subsection
    fields = '__all__'


class SubsectionUpdateView(ProtectedUpdateView):
    model = Subsection
    fields = '__all__'


class SubsectionDeleteView(ProtectedDeleteView):
    model = Subsection


class SubsectionCreateQuestionView(ProtectedCreateView):
    model = Question
    fields = ['order', 'text_en', 'text_de', 'widget_type']

    def dispatch(self, *args, **kwargs):
        self.subsection = get_object_or_404(Subsection, pk=self.kwargs['pk'])
        return super(SubsectionCreateQuestionView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.subsection = self.subsection
        return super(SubsectionCreateQuestionView, self).form_valid(form)


class SubsectionCreateQuestionSetView(ProtectedCreateView):
    model = QuestionSet
    fields = ['order', 'title_en', 'title_de']

    def dispatch(self, *args, **kwargs):
        self.subsection = get_object_or_404(Subsection, pk=self.kwargs['pk'])
        return super(SubsectionCreateQuestionSetView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.subsection = self.subsection
        return super(SubsectionCreateQuestionSetView, self).form_valid(form)


class QuestionCreateView(ProtectedCreateView):
    model = Question
    fields = '__all__'


class QuestionUpdateView(ProtectedUpdateView):
    model = Question
    fields = '__all__'


class QuestionDeleteView(ProtectedDeleteView):
    model = Question


class QuestionSetCreateView(ProtectedCreateView):
    model = QuestionSet
    fields = '__all__'


class QuestionSetUpdateView(ProtectedUpdateView):
    model = QuestionSet
    fields = '__all__'


class QuestionSetDeleteView(ProtectedDeleteView):
    model = QuestionSet


class QuestionSetCreateQuestionView(ProtectedCreateView):
    model = Question
    fields = ['order', 'text_en', 'text_de', 'widget_type']

    def dispatch(self, *args, **kwargs):
        self.questionset = get_object_or_404(QuestionSet, pk=self.kwargs['pk'])
        return super(QuestionSetCreateQuestionView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.subsection = self.questionset.subsection
        form.instance.questionset = self.questionset
        return super(QuestionSetCreateQuestionView, self).form_valid(form)


# def questions_sequence_gv(request):
#     content = render_to_string('questions/questions_sequence.gv', {
#         'sections': Section.objects.all(),
#         'question_ids': [question.pk for question in Question.objects.all()]
#     })

#     # remove empty lines
#     # content = "".join([s for s in content.strip().splitlines(True) if s.strip()])

#     return HttpResponse(content, content_type='text/plain')