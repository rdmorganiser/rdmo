from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets, filters

from apps.core.views import ProtectedCreateView, ProtectedUpdateView, ProtectedDeleteView

from .models import *
from .serializers import *


def catalogs(request):
    return render(request, 'questions/catalogs.html', {'catalogs': Catalog.objects.all()})


def catalog(request, pk):
    catalog = get_object_or_404(Catalog, pk=pk)
    return render(request, 'questions/catalog.html', {'catalog': catalog})


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


class SectionCreateView(ProtectedCreateView):
    model = Section
    fields = '__all__'


class SectionUpdateView(ProtectedUpdateView):
    model = Section
    fields = '__all__'


class SectionDeleteView(ProtectedDeleteView):
    model = Section

    def get_success_url(self):
        return self.object.get_absolute_url()


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

    def get_success_url(self):
        return self.object.get_absolute_url()


class SubsectionCreateQuestionView(ProtectedCreateView):
    model = Question
    fields = ['order', 'attribute', 'text_en', 'text_de', 'widget_type']

    def dispatch(self, *args, **kwargs):
        self.subsection = get_object_or_404(Subsection, pk=self.kwargs['pk'])
        return super(SubsectionCreateQuestionView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.subsection = self.subsection
        return super(SubsectionCreateQuestionView, self).form_valid(form)


class SubsectionCreateQuestionSetView(ProtectedCreateView):
    model = QuestionSet
    fields = ['order', 'attributeset', 'title_en', 'title_de', 'help_en', 'help_de']

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
    success_url = reverse_lazy('catalogs')

    def get_success_url(self):
        return self.object.get_absolute_url()


class QuestionSetCreateView(ProtectedCreateView):
    model = QuestionSet
    fields = '__all__'


class QuestionSetUpdateView(ProtectedUpdateView):
    model = QuestionSet
    fields = '__all__'


class QuestionSetDeleteView(ProtectedDeleteView):
    model = QuestionSet
    success_url = reverse_lazy('catalogs')

    def get_success_url(self):
        return self.object.get_absolute_url()


class QuestionSetCreateQuestionView(ProtectedCreateView):
    model = Question
    fields = ['order', 'attribute', 'widget_type', 'text_en', 'text_de', 'title_en', 'title_de']

    def dispatch(self, *args, **kwargs):
        self.questionset = get_object_or_404(QuestionSet, pk=self.kwargs['pk'])
        return super(QuestionSetCreateQuestionView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.subsection = self.questionset.subsection
        form.instance.questionset = self.questionset
        return super(QuestionSetCreateQuestionView, self).form_valid(form)


def questions(request):
    return render(request, 'questions/questions.html')


class CatalogViewSet(viewsets.ModelViewSet):

    queryset = Catalog.objects.all().order_by('pk')
    serializer_class = CatalogSerializer


class QuestionSetViewSet(viewsets.ModelViewSet):

    queryset = QuestionSet.objects.all()
    serializer_class = QuestionSetSerializer


class QuestionViewSet(viewsets.ModelViewSet):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionEntityViewSet(viewsets.ModelViewSet):

    queryset = QuestionEntity.objects.filter(question__questionset=None).order_by('order')
    serializer_class = QuestionEntitySerializer

    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('subsection', )
