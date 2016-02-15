from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render

from apps.core.views import ProtectedUpdateView, ProtectedDeleteView
from apps.projects.models import Project
from apps.questions.models import *

from .models import *
from .forms import *


def interview(request, pk):
    interview = Interview.objects.get(pk=pk)
    sections = Section.objects.all()
    answers_dict = {}
    for answer in interview.answers.all():
        answers_dict[answer.question.pk] = answer

    return render(request, 'interviews/interview.html', {'interview': interview, 'sections': sections, 'answers_dict': answers_dict})


def interview_create(request, project_id):

    try:
        project = Project.objects.filter(owner=request.user).get(pk=project_id)
    except Project.DoesNotExist:
        raise Http404(_('Project not found'))

    if request.method == 'POST':
        form = InterviewForm(request.POST)

        if form.is_valid():
            interview = Interview()
            interview.project = project
            interview.title = form.cleaned_data['title']
            interview.completed = False
            interview.save()

            return HttpResponseRedirect(reverse('interview_start', kwargs={'interview_id': interview.pk}))
    else:
        form = InterviewForm()

    return render(request, 'interviews/interview_form.html', {'form': form, 'project': project, 'create': True})


class InterviewUpdateView(ProtectedUpdateView):
    model = Interview
    fields = ('title', )

    def get_queryset(self):
        return Interview.objects.filter(project__owner=self.request.user)

    def get_success_url(self):
        return reverse('interview', kwargs={'pk': self.object.pk})


class InterviewDeleteView(ProtectedDeleteView):
    model = Interview

    def get_queryset(self):
        return Interview.objects.filter(project__owner=self.request.user)

    def get_success_url(self):
        return reverse('project', kwargs={'pk': self.object.project.pk})


def interview_start(request, interview_id):
    first_group = Group.objects.first()

    if first_group is not None:
        return HttpResponseRedirect(reverse('interview_group', kwargs={
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
        return HttpResponseRedirect(reverse('interview_group', kwargs={
            'interview_id': interview_id,
            'group_id': interview.current_group.pk
        }))


def interview_group(request, interview_id, group_id):
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

    print(questions)

    if request.method == 'POST':
        form = GroupForm(request.POST, questions=questions, answers=answers)

        if form.is_valid():
            for question, answer in zip(questions, answers):
                if not answer:
                    answer = Answer(interview=interview, question=question)

                answer.value = form.cleaned_data[question.slug]
                answer.save()

            try:
                interview.current_group = Group.objects.get_next(group)
                interview.save()

                return HttpResponseRedirect(reverse('interview_group', kwargs={
                    'interview_id': interview.pk,
                    'group_id': interview.current_group.pk
                }))
            except Group.DoesNotExist:
                interview.current_group = None
                interview.completed = True
                interview.save()

                return HttpResponseRedirect(reverse('interview_done', kwargs={'interview_id': interview.pk}))

    else:
        form = GroupForm(questions=questions, answers=answers)

    return render(request, 'interviews/interview_group.html', {'form': form})


def interview_done(request, interview_id):
    return render(request, 'interviews/interview_done.html', {'interview_id': interview_id})
