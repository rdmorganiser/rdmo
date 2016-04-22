from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from apps.core.views import ProtectedCreateView, ProtectedUpdateView, ProtectedDeleteView
from apps.questions.views import QuestionEntity

from .models import *
from .serializers import *


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
def project_questions_form(request, project_id, question_entity_id=None):
    project = Project.objects.get(pk=project_id)

    question_entities = QuestionEntity.objects.order_by_catalog(project.catalog)

    if question_entity_id:
        question_entity = get_object_or_404(QuestionEntity, pk=question_entity_id)
    else:
        return HttpResponseRedirect(reverse('project_questions_form', kwargs={
            'project_id': project_id,
            'question_entity_id': question_entities.first().pk
        }))

    progress, has_prev, has_next = question_entities.get_progress(question_entity.pk)

    context = {
        'project': project,
        'question_entity': question_entity,
        'progress': progress
    }

    options = {
        'snapshot': {
            'id': project.current_snapshot.pk
        },
        'has_prev': has_prev,
        'has_next': has_next
    }

    if question_entity.is_set:
        questionset = question_entity.questionset

        context['question'] = False
        context['questionset'] = questionset

        options['attribute'] = False
        options['attributeset'] = {
            'id': questionset.attributeset.pk,
            'tag': questionset.attributeset.tag,
            'is_collection': questionset.attributeset.is_collection,
            'attributes': [{
                'id': question.attribute.pk,
                'tag': question.attribute.tag,
                'is_collection': question.attribute.is_collection
            } for question in questionset.questions.all()]
        }

    else:
        question = question_entity.question

        context['question'] = question
        context['questionset'] = False

        options['attribute'] = {
            'id': question.attribute.pk,
            'tag': question.attribute.tag,
            'is_collection': question.attribute.is_collection
        }
        options['attributeset'] = False

    context['options_json'] = json.dumps(options)

    return render(request, 'projects/project_questions_form.html', context)


@login_required()
def project_questions_prev(request, project_id, question_entity_id):
    project = Project.objects.get(pk=project_id)
    prev_question_entity = QuestionEntity.objects.order_by_catalog(project.catalog).get_prev(question_entity_id)

    return HttpResponseRedirect(reverse('project_questions_form', kwargs={
        'project_id': project_id,
        'question_entity_id': prev_question_entity.pk
    }))


@login_required()
def project_questions_next(request, project_id, question_entity_id):
    project = Project.objects.get(pk=project_id)
    next_question_entity = QuestionEntity.objects.order_by_catalog(project.catalog).get_next(question_entity_id)

    return HttpResponseRedirect(reverse('project_questions_form', kwargs={
        'project_id': project_id,
        'question_entity_id': next_question_entity.pk
    }))


@login_required()
def project_questions_done(request, project_id):
    return render(request, 'projects/project_questions_done.html', {
        'project_id': project_id
    })




@login_required()
def project_questions(request, project_id, entity_id=None):
    return render(request, 'projects/project_questions.html', {
        'project_id': project_id,
        'entity_id': entity_id
    });


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )

    serializer_class = ProjectsSerializer

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)


class ValueViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )

    serializer_class = ValueSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('attribute', 'attribute__tag', 'valueset')

    def get_queryset(self):
        return Value.objects.filter(snapshot__project__owner=self.request.user).order_by('index')


class ValueSetViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )

    serializer_class = ValueSetSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('attributeset', 'attributeset__tag', )

    def get_queryset(self):
        return ValueSet.objects.filter(snapshot__project__owner=self.request.user).order_by('index')








