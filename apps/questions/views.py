from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.template.loader import render_to_string

from apps.core.views import ProtectedCreateView, ProtectedUpdateView, ProtectedDeleteView

from .models import *


def questions(request):
    return render(request, 'questions/questions.html', {'sections': Section.objects.all()})


def questions_sequence_gv(request):
    content = render_to_string('questions/questions_sequence.gv', {
        'sections': Section.objects.all(),
        'question_ids': [question.pk for question in Question.objects.all()]
    })

    # remove empty lines
    # content = "".join([s for s in content.strip().splitlines(True) if s.strip()])

    return HttpResponse(content, content_type='text/plain')


class SectionCreateView(ProtectedCreateView):
    model = Section
    fields = '__all__'
    success_url = reverse_lazy('questions')


class SectionUpdateView(ProtectedUpdateView):
    model = Section
    fields = '__all__'
    success_url = reverse_lazy('questions')


class SectionDeleteView(ProtectedDeleteView):
    model = Section
    success_url = reverse_lazy('questions')


class SubsectionCreateView(ProtectedCreateView):
    model = Subsection
    fields = '__all__'
    success_url = reverse_lazy('questions')

    def get_form_kwargs(self):
        kwargs = super(SubsectionCreateView, self).get_form_kwargs()
        if 'pk' in self.kwargs:
            kwargs['initial']['section'] = Section.objects.get(pk=self.kwargs['pk'])
        return kwargs


class SubsectionUpdateView(ProtectedUpdateView):
    model = Subsection
    fields = '__all__'
    success_url = reverse_lazy('questions')


class SubsectionDeleteView(ProtectedDeleteView):
    model = Subsection
    success_url = reverse_lazy('questions')


class GroupCreateView(ProtectedCreateView):
    model = Group
    fields = '__all__'
    success_url = reverse_lazy('questions')

    def get_form_kwargs(self):
        kwargs = super(GroupCreateView, self).get_form_kwargs()
        if 'pk' in self.kwargs:
            kwargs['initial']['subsection'] = Subsection.objects.get(pk=self.kwargs['pk'])
        return kwargs


class GroupUpdateView(ProtectedUpdateView):
    model = Group
    fields = '__all__'
    success_url = reverse_lazy('questions')


class GroupDeleteView(ProtectedDeleteView):
    model = Group
    success_url = reverse_lazy('questions')


class QuestionCreateView(ProtectedCreateView):
    model = Question
    fields = '__all__'
    success_url = reverse_lazy('questions')

    def get_form_kwargs(self):
        kwargs = super(QuestionCreateView, self).get_form_kwargs()
        if 'pk' in self.kwargs:
            kwargs['initial']['group'] = Group.objects.get(pk=self.kwargs['pk'])
        return kwargs


class QuestionUpdateView(ProtectedUpdateView):
    model = Question
    fields = '__all__'
    success_url = reverse_lazy('questions')


class QuestionDeleteView(ProtectedDeleteView):
    model = Question
    success_url = reverse_lazy('questions')
