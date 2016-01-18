from django.shortcuts import render

from .models import Interview


def interview(request, pk):
    interview = Interview.objects.get(pk=pk)
    return render(request, 'interviews/interview.html', {'interview': interview})


def interview_create(request):
    return render(request, 'interviews/interview_create.html')


def interview_update(request, pk):
    return render(request, 'interviews/interview_update.html')


def interview_delete(request, pk):
    return render(request, 'interviews/interview_delete.html')
