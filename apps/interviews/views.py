from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string

from apps.core.views import ProtectedCreateView, ProtectedUpdateView, ProtectedDeleteView
from apps.projects.models import Project

from .models import Interview, Section, Subsection, Question, Answer
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


def interview_questions(request, interview_id, answer_id=None):

    interview = Interview.objects.get(pk=interview_id)
    answers = Answer.objects.filter(interview=interview)

    if answers:
        last_question = answers.last().question
        question = Question.objects.get_next(last_question)
    else:
        question = Question.objects.first()

    if question:
        if request.method == 'POST':
            form = QuestionForm(request.POST, question=question)

            if form.is_valid():
                answer = Answer(interview=interview, question=question)
                answer.value = form.cleaned_data['answer']
                answer.save()

                return HttpResponseRedirect(reverse('interview_questions', kwargs={'interview_id': interview.pk}))

        else:
            form = QuestionForm(question=question)

        return render(request, 'interviews/interview_questions.html', {'form': form})

    else:
        return HttpResponseRedirect(reverse('interview_done', kwargs={'interview_id': interview.pk}))


def interview_resume(request, interview_id, answer_id=None):

    if answer_id:
        try:
            answer = Answer.objects.filter(interview_id=interview_id).filter(answer_id=answer_id)
            question = answer.next_question
        except Answer.DoesNotExist:
            return render(request, 'interviews/interview_resume.html')
    else:
        question = Question.objects.first()

    request.session['interview_current_question_id'] = question.pk

    return render(request, 'interviews/interview_done.html', {'interview_id': interview_id})


def interview_done(request, interview_id):
    return render(request, 'interviews/interview_done.html', {'interview_id': interview_id})


def interview_update(request, pk):
    return render(request, 'interviews/interview_update.html')


def interview_delete(request, pk):
    return render(request, 'interviews/interview_delete.html')


def questions(request):
    return render(request, 'interviews/questions.html', {'sections': Section.objects.all()})


def questions_sequence_gv(request):
    content = render_to_string('interviews/questions_sequence.gv', {
        'sections': Section.objects.all(),
        'question_ids': [question.pk for question in Question.objects.all()]
    })

    # remove empty lines
    # content = "".join([s for s in content.strip().splitlines(True) if s.strip()])

    return HttpResponse(content, content_type='text/plain')


def question(request, pk):
    return render(request, 'interviews/question.html', {'question': Question.objects.get(pk=pk)})


class QuestionCreateView(ProtectedCreateView):
    model = Question
    fields = '__all__'
    success_url = reverse_lazy('questions')


class QuestionUpdateView(ProtectedUpdateView):
    model = Question
    fields = '__all__'
    success_url = reverse_lazy('questions')


class QuestionDeleteView(ProtectedDeleteView):
    model = Question
    success_url = reverse_lazy('questions')


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


class SubsectionUpdateView(ProtectedUpdateView):
    model = Subsection
    fields = '__all__'
    success_url = reverse_lazy('questions')


class SubsectionDeleteView(ProtectedDeleteView):
    model = Subsection
    success_url = reverse_lazy('questions')
