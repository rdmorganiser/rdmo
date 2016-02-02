from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string

from apps.core.views import ProtectedCreateView, ProtectedUpdateView, ProtectedDeleteView
from apps.projects.models import Project

from .models import Interview, Topic, Category, Question, Answer
from .forms import InterviewCreateForm, QuestionForm


def interview(request, pk):
    interview = Interview.objects.get(pk=pk)
    return render(request, 'interviews/interview.html', {'interview': interview})


def interview_create(request):

    if request.method == 'POST':
        form = InterviewCreateForm(request.POST)
        form.fields["project"].queryset = Project.objects.filter(owner=request.user)

        if form.is_valid():
            interview = Interview()
            interview.project = form.cleaned_data['project']
            interview.title = form.cleaned_data['title']
            interview.save()

            return HttpResponseRedirect(reverse('interview_question', kwargs={
                'interview_id': interview.pk,
                'question_id': Question.objects.get_first().pk
            }))

    else:
        form = InterviewCreateForm()
        form.fields["project"].queryset = Project.objects.filter(owner=request.user)

    return render(request, 'interviews/interview_create.html', {'form': form})


def interview_question(request, interview_id, question_id):

    interview = Interview.objects.get(pk=interview_id)
    question = Question.objects.get(pk=question_id)

    if request.method == 'POST':
        form = QuestionForm(request.POST, question=question)

        if form.is_valid():
            answer = Answer(interview=interview, question=question)
            answer.answer = form.cleaned_data['answer']
            answer.save()

            return HttpResponseRedirect(reverse('interview_question', kwargs={'interview_id': interview.pk, 'question_id': question.next_question.pk}))

    else:
        form = QuestionForm(question=question)

    return render(request, 'interviews/interview_question.html', {'form': form})


def interview_update(request, pk):
    return render(request, 'interviews/interview_update.html')


def interview_delete(request, pk):
    return render(request, 'interviews/interview_delete.html')


def questions(request):
    return render(request, 'interviews/questions.html', {'topics': Topic.objects.all()})


def questions_sequence_dot(request):
    content = render_to_string('interviews/questions_sequence_dot.html', {'topics': Topic.objects.all()})
    return HttpResponse(content, content_type='text/plain')


def question(request, pk):
    return render(request, 'interviews/question.html', {'question': Question.objects.get(pk=pk)})


class QuestionCreateView(ProtectedCreateView):
    model = Question
    fields = '__all__'


class QuestionUpdateView(ProtectedUpdateView):
    model = Question
    fields = '__all__'


class QuestionDeleteView(ProtectedDeleteView):
    model = Question
    success_url = reverse_lazy('questions')

