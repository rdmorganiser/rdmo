from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Project


@login_required()
def projects(request):
    projects = Project.objects.filter(owner=request.user)
    return render(request, 'projects/projects.html', {'projects': projects})


@login_required()
def project(request, pk):
    project = Project.objects.get(pk=pk)
    return render(request, 'projects/project.html', {'project': project})
