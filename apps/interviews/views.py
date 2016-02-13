from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template.loader import render_to_string

from apps.core.views import ProtectedCreateView, ProtectedUpdateView, ProtectedDeleteView
from apps.projects.models import Project

from .models import *
from .forms import InterviewCreateForm, InterviewForm


def interview(request, pk):
    interview = Interview.objects.get(pk=pk)
    return render(request, 'interviews/interview.html', {'interview': interview})


def interview_create(request, project_id):

    try:
        project = Project.objects.filter(owner=request.user).get(pk=project_id)
    except Project.DoesNotExist:
        raise Http404(_('Project not found'))

    if request.method == 'POST':
        form = InterviewCreateForm(request.POST)

        if form.is_valid():
            interview = Interview()
            interview.project = project
            interview.title = form.cleaned_data['title']
            interview.completed = False
            interview.save()

            return HttpResponseRedirect(reverse('interview_start', kwargs={'interview_id': interview.pk}))
    else:
        form = InterviewCreateForm()

    return render(request, 'interviews/interview_create.html', {'form': form, 'project': project})


def interview_start(request, interview_id):
    first_group = Group.objects.first()

    if first_group is not None:
        return HttpResponseRedirect(reverse('interview_form', kwargs={
            'interview_id': interview_id,
            'group_id': Group.objects.first().pk
        }))
    else:
        return HttpResponseRedirect(reverse('interview_done', kwargs={'interview_id': interview_id}))


def interview_resume(request, interview_id):
    interview = Interview.objects.get(pk=interview_id)

    if interview.completed:
        return HttpResponseRedirect(reverse('interview_done', kwargs={'interview_id': interview.pk}))
    elif interview.current_group is None:
        return HttpResponseRedirect(reverse('interview_start', kwargs={'interview_id': interview.pk}))
    else:
        return HttpResponseRedirect(reverse('interview_form', kwargs={
            'interview_id': interview_id,
            'group_id': interview.current_group.pk
        }))


def interview_form(request, interview_id, group_id):
    interview = Interview.objects.get(pk=interview_id)
    group = Group.objects.get(pk=group_id)

    questions = group.questions.all()
    answers = []
    for question in questions:
        try:
            answer = Answer.objects.get(interview=interview, question=question)
        except Answer.DoesNotExist:
            answer = None
        answers.append(answer)

    if request.method == 'POST':
        form = InterviewForm(request.POST, questions=questions, answers=answers)

        if form.is_valid():
            for question, answer in zip(questions, answers):
                if not answer:
                    answer = Answer(interview=interview, question=question)

                answer.value = form.cleaned_data[question.slug]
                answer.save()

            try:
                interview.current_group = Group.objects.get_next(group)
                interview.save()

                return HttpResponseRedirect(reverse('interview_form', kwargs={
                    'interview_id': interview.pk,
                    'group_id': interview.current_group.pk
                }))
            except Group.DoesNotExist:
                interview.current_group = None
                interview.completed = True
                interview.save()

                return HttpResponseRedirect(reverse('interview_done', kwargs={'interview_id': interview.pk}))

    else:
        form = InterviewForm(questions=questions, answers=answers)

    return render(request, 'interviews/interview_questions.html', {'form': form})


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
