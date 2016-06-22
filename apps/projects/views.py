from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from apps.core.views import ProtectedCreateView, ProtectedUpdateView, ProtectedDeleteView
# from apps.questions.views import QuestionEntity

from .models import Project
from .serializers import *
from .utils import get_answer_tree


@login_required()
def projects(request):
    projects = Project.objects.filter(owner=request.user)
    return render(request, 'projects/projects.html', {'projects': projects})


@login_required()
def project(request, pk):
    project = Project.objects.get(pk=pk)
    return render(request, 'projects/project.html', {'project': project})


@login_required()
def project_summary(request, pk):
    project = Project.objects.get(pk=pk)

    return render(request, 'projects/project_summary.html', {
        'project': project,
        'answer_tree': get_answer_tree(project)
    })


class ProjectCreateView(ProtectedCreateView):
    model = Project
    fields = ['title', 'description', 'catalog']

    def form_valid(self, form):
        response = super(ProjectCreateView, self).form_valid(form)

        # add current user as owner
        form.instance.owner.add(self.request.user)

        return response


class ProjectUpdateView(ProtectedUpdateView):
    model = Project
    fields = ['title', 'description', 'catalog']


class ProjectDeleteView(ProtectedDeleteView):
    model = Project
    success_url = reverse_lazy('projects')


@login_required()
def project_questions(request, project_id):
    return render(request, 'projects/project_questions.html', {
        'project_id': project_id
    })


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )

    serializer_class = ProjectsSerializer

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)


class ValueViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )

    serializer_class = ValueSerializer

    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = (
        'snapshot',
        'attribute',
        'attribute__parent_collection'
    )

    def get_queryset(self):
        return Value.objects \
            .filter(snapshot__project__owner=self.request.user) \
            .order_by('set_index', 'collection_index')
