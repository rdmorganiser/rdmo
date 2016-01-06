from django.shortcuts import render

from .models import Interview


def interview_create(request):

    return render(request, 'interviews/interview_create.html')
