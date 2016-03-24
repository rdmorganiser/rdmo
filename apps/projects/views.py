import json

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy

from rest_framework import viewsets, mixins, filters

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

    question_entities = QuestionEntity.objects \
        .filter(subsection__section__catalog=project.catalog) \
        .filter(question__questionset=None) \
        .order_by('subsection__section__order', 'subsection__order', 'order')

    question_entity_id_list = list(question_entities.values_list('pk', flat=True))

    if question_entity_id:
        question_entity = get_object_or_404(QuestionEntity, pk=question_entity_id)
    else:
        return HttpResponseRedirect(reverse('project_questions_form', kwargs={
            'project_id': project_id,
            'question_entity_id': question_entity_id_list[0]
        }))

    current_index = question_entity_id_list.index(question_entity.pk)
    prev_question_entity_id = question_entity_id_list[current_index - 1] if current_index > 0 else None
    next_question_entity_id = question_entity_id_list[current_index + 1] if current_index + 1 < len(question_entity_id_list) else None

    context = {
        'project': project,
        'title': question_entity.title,
        'progress': (100.0 * (1 + current_index)/len(question_entity_id_list))
    }

    options = {
        'snapshot': {
            'id': project.current_snapshot.pk
        },
        'prev': False if prev_question_entity_id is None else True,
        'next': False if next_question_entity_id is None else True
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

    # if question_entity.is_set:
    #     # get all valuesets for this questionset
    #     valuesets = ValueSet.objects.filter(
    #         snapshot=project.current_snapshot,
    #         attributeset=question_entity.questionset.attributeset
    #     )

    #     # there should be at least one valueset
    #     if not valuesets:
    #         valueset = ValueSet.objects.create(snapshot=project.current_snapshot, attributeset=question_entity.questionset.attributeset)
    #         valuesets = [valueset]

    #     # create values in those valuesets
    #     for valueset in valuesets:
    #         for question in question_entity.questionset.questions.all():
    #             Value.objects.get_or_create(
    #                 snapshot=project.current_snapshot,
    #                 attribute=question.attribute,
    #                 valueset=valueset
    #             )

    #     values = {}
    #     for valueset in valuesets:
    #         for question in question_entity.questionset.questions.all():
    #             values['%s[%i]' % (question.tag, valueset.index)] = Value.objects.get_or_create(
    #                 snapshot=project.current_snapshot,
    #                 attribute=question.attribute,
    #                 valueset=valueset
    #             )

    # else:
    #     # get or create value for this question
    #     value, created = Value.objects.get_or_create(
    #         snapshot=project.current_snapshot,
    #         attribute=question_entity.question.attribute
    #     )

    # if request.method == 'POST':
    #     if request.POST.get('prev'):
    #         return HttpResponseRedirect(reverse('project_questions_form', kwargs={
    #             'project_id': project_id,
    #             'question_entity_id': prev_question_entity_id
    #         }))
    #     elif request.POST.get('next'):
    #         return HttpResponseRedirect(reverse('project_questions_form', kwargs={
    #             'project_id': project_id,
    #             'question_entity_id': next_question_entity_id
    #         }))
    #     else:
    #         if question_entity.is_set:
    #             form = QuestionSetForm(request.POST, questionset=question_entity.questionset, valuesets=valuesets)
    #         else:
    #             form = QuestionForm(request.POST, question=question_entity.question, value=value)

    #         if form.is_valid():
    #             if question_entity.is_set:
    #                 # for a questionset, loop over values and save them
    #                 for valueset in valuesets:
    #                     for value in valueset.values.all():
    #                         value.text = form.cleaned_data['%s[%i]' % (value.tag, valueset.index)]
    #                         value.save()

    #             else:
    #                 # for a single question, just save the new value
    #                 value.text = form.cleaned_data[value.tag]
    #                 value.save()

    #             if request.POST.get('save_next'):
    #                 return HttpResponseRedirect(reverse('project_questions_form', kwargs={
    #                     'project_id': project_id,
    #                     'question_entity_id': next_question_entity_id
    #                 }))
    #             elif request.POST.get('save_finish'):
    #                 return HttpResponseRedirect(reverse('project_questions_done', kwargs={
    #                     'project_id': project_id,
    #                 }))
    # else:
    #     if question_entity.is_set:
    #         form = QuestionSetForm(questionset=question_entity.questionset, valuesets=valuesets)
    #     else:
    #         form = QuestionForm(question=question_entity.question, value=value)


@login_required()
def project_questions_done(request, project_id):
    return render(request, 'projects/project_questions_done.html', {
        'project_id': project_id
    })


class ValueViewSet(viewsets.ModelViewSet):

    serializer_class = ValueSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('attribute', 'attribute__tag', 'valueset')

    def get_queryset(self):
        return Value.objects.filter(snapshot__project__owner=self.request.user).order_by('index')


class ValueSetViewSet(viewsets.ModelViewSet):

    serializer_class = ValueSetSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('attributeset', 'attributeset__tag', )

    def get_queryset(self):
        return ValueSet.objects.filter(snapshot__project__owner=self.request.user).order_by('index')
