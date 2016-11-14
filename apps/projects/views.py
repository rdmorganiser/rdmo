from django.conf import settings
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.template import TemplateSyntaxError
from django.utils.translation import ugettext_lazy as _

from rest_framework import viewsets, filters
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.exceptions import ValidationError

from apps.core.views import ProtectedCreateView, ProtectedUpdateView, ProtectedDeleteView
from apps.core.utils import render_to_format

from apps.tasks.models import Task
from apps.views.models import View

from .models import Project, Snapshot, Value
from .serializers import *
from .utils import get_answers_tree


@login_required()
def projects(request):
    projects = Project.objects.filter(owner=request.user)
    return render(request, 'projects/projects.html', {'projects': projects})


@login_required()
def project(request, pk):
    project = get_object_or_404(Project.objects.filter(owner=request.user), pk=pk)

    tasks = []
    for task in Task.objects.all():
        for condition in task.conditions.all():
            if condition.resolve(project):
                tasks.append({
                    'title': task.title,
                    'text': task.text,
                    'deadline': task.get_deadline(project),
                })

    return render(request, 'projects/project.html', {
        'project': project,
        'tasks': tasks,
        'views': View.objects.all(),
        'snapshots': project.snapshots.all()
    })


@login_required()
def project_answers(request, project_id, snapshot_id=None):
    project = get_object_or_404(Project.objects.filter(owner=request.user), pk=project_id)
    snapshots = list(project.snapshots.values('id', 'title'))

    try:
        current_snapshot = project.snapshots.get(pk=snapshot_id)
    except Snapshot.DoesNotExist:
        current_snapshot = None

    return render(request, 'projects/project_answers.html', {
        'project': project,
        'snapshots': snapshots,
        'current_snapshot': current_snapshot,
        'answers_tree': get_answers_tree(project, current_snapshot),
        'export_formats': settings.EXPORT_FORMATS
    })


@login_required()
def project_answers_export(request, format, project_id, snapshot_id=None):
    project = get_object_or_404(Project.objects.filter(owner=request.user), pk=project_id)

    try:
        current_snapshot = project.snapshots.get(pk=snapshot_id)
    except Snapshot.DoesNotExist:
        current_snapshot = None

    return render_to_format(request, format, project.title, 'projects/project_answers_export.html', {
        'project': project,
        'answers_tree': get_answers_tree(project, current_snapshot)
    })


@login_required()
def project_view(request, project_id, view_id, snapshot_id=None):
    project = get_object_or_404(Project.objects.filter(owner=request.user), pk=project_id)
    snapshots = list(project.snapshots.values('id', 'title'))

    try:
        current_snapshot = project.snapshots.get(pk=snapshot_id)
    except Snapshot.DoesNotExist:
        current_snapshot = None

    view = get_object_or_404(View.objects.all(), pk=view_id)

    try:
        rendered_view = view.render(project, current_snapshot)
    except TemplateSyntaxError:
        rendered_view = None

    return render(request, 'projects/project_view.html', {
        'project': project,
        'snapshots': snapshots,
        'current_snapshot': current_snapshot,
        'view': view,
        'rendered_view': rendered_view,
        'export_formats': settings.EXPORT_FORMATS
    })


@login_required()
def project_view_export(request, project_id, view_id, format, snapshot_id=None):
    project = get_object_or_404(Project.objects.filter(owner=request.user), pk=project_id)

    try:
        current_snapshot = project.snapshots.get(pk=snapshot_id)
    except Snapshot.DoesNotExist:
        current_snapshot = None

    view = get_object_or_404(View.objects.all(), pk=view_id)

    try:
        rendered_view = view.render(project, current_snapshot)
    except TemplateSyntaxError:
        rendered_view = None

    return render_to_format(request, format, view.title, 'projects/project_view_export.html', {
        'project': project,
        'rendered_view': rendered_view
    })


@login_required()
def project_questions(request, project_id):
    return render(request, 'projects/project_questions.html', {
        'project_id': project_id
    })


def snapshot_rollback(request, project_id, snapshot_id):
    project = get_object_or_404(Project.objects.filter(owner=request.user), pk=project_id)

    try:
        current_snapshot = project.snapshots.get(pk=snapshot_id)
    except Snapshot.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        if 'cancel' not in request.POST:
            current_snapshot.rollback()

        return HttpResponseRedirect(reverse('project', args=[project.id]))

    return render(request, 'projects/snapshot_rollback.html', {
        'current_snapshot': current_snapshot
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

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)


class ProjectDeleteView(ProtectedDeleteView):
    model = Project
    success_url = reverse_lazy('projects')

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)


class SnapshotCreateView(ProtectedCreateView):
    model = Snapshot
    fields = ['title', 'description']

    def dispatch(self, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.filter(owner=self.request.user), pk=self.kwargs['project_id'])
        return super(SnapshotCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.project = self.project
        return super(SnapshotCreateView, self).form_valid(form)


class SnapshotUpdateView(ProtectedUpdateView):
    model = Snapshot
    fields = ['title', 'description']

    def get_queryset(self):
        return Snapshot.objects.filter(project__owner=self.request.user)


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
        'attribute',
        'attribute__parent_collection'
    )

    def get_queryset(self):
        queryset = Value.objects

        if hasattr(self, 'project'):
            queryset = queryset.filter(project=self.project)

            if hasattr(self, 'snapshot'):
                queryset = queryset.filter(snapshot=self.snapshot)
            else:
                queryset = queryset.filter(snapshot=None)

            queryset = queryset.order_by('set_index', 'collection_index')
        else:
            queryset = queryset.filter(project__owner=self.request.user)

        return queryset

    def get_project(self, project_id):
        if project_id is None:
            raise ValidationError({'project': [_('This field is required.')]})
        else:
            try:
                return Project.objects.filter(owner=self.request.user).get(pk=project_id)
            except Project.DoesNotExist as e:
                raise ValidationError({'project': [e.message]})

    def get_snapshot(self, snapshot_id):
        if snapshot_id is None:
            return None
        else:
            try:
                return self.project.snapshots.get(pk=snapshot_id)
            except Snapshot.DoesNotExist as e:
                raise ValidationError({'snapshot': [e.message]})

    def get_condition(self, condition_id):
        if condition_id is None:
            raise ValidationError({'condition': [_('This field is required.')]})
        else:
            try:
                return Condition.objects.get(pk=condition_id)
            except Condition.DoesNotExist as e:
                raise ValidationError({'condition': [e.message]})

    def list(self, request, *args, **kwargs):
        self.project = self.get_project(request.GET.get('project'))
        self.snapshot = self.get_snapshot(request.GET.get('snapshot'))

        return super(ValueViewSet, self).list(request, args, kwargs)

    @list_route()
    def resolve(self, request):
        self.project = self.get_project(request.GET.get('project'))
        self.snapshot = self.get_snapshot(request.GET.get('snapshot'))
        condition = self.get_condition(request.GET.get('condition'))

        return Response({'result': condition.resolve(self.project, self.snapshot)})


class QuestionEntityViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = QuestionEntity.objects.filter(question__parent=None)
    serializer_class = QuestionEntitySerializer

    @list_route(methods=['get'], permission_classes=[DjangoModelPermissions])
    def first(self, request, pk=None):
        try:
            catalog = Catalog.objects.get(pk=request.GET.get('catalog'))
            entity = QuestionEntity.objects.order_by_catalog(catalog).first()
            serializer = self.get_serializer(entity)
            return Response(serializer.data)
        except Catalog.DoesNotExist as e:
            return Response({'message': e.message}, status=HTTP_404_NOT_FOUND)

    @detail_route(methods=['get'], permission_classes=[DjangoModelPermissions])
    def prev(self, request, pk=None):
        try:
            return Response({'id': QuestionEntity.objects.get_prev(pk).pk})
        except QuestionEntity.DoesNotExist as e:
            return Response({'message': e.message}, status=HTTP_404_NOT_FOUND)

    @detail_route(methods=['get'], permission_classes=[DjangoModelPermissions])
    def next(self, request, pk=None):
        try:
            return Response({'id': QuestionEntity.objects.get_next(pk).pk})
        except QuestionEntity.DoesNotExist as e:
            return Response({'message': e.message}, status=HTTP_404_NOT_FOUND)


class CatalogViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated, )

    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer
