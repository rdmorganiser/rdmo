from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy

from apps.core.views import ProtectedCreateView, ProtectedUpdateView, ProtectedDeleteView
from .models import Project


@login_required()
def projects(request):
    projects = Project.objects.filter(owner=request.user)
    return render(request, 'projects/projects.html', {'projects': projects})


@login_required()
def project(request, pk):
    project = Project.objects.get(pk=pk)
    return render(request, 'projects/project.html', {'project': project})


class ProjectCreateView(ProtectedCreateView):
    model = Project
    fields = ['name', 'pi', 'description']
    success_url = '/thanks/'


class ProjectUpdateView(ProtectedUpdateView):
    model = Project
    fields = ['name', 'pi', 'description']


class ProjectDeleteView(ProtectedDeleteView):
    model = Project
    success_url = reverse_lazy('projects')
