from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import prefetch_related_objects
from django.http import Http404, HttpResponseRedirect
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_extensions.mixins import NestedViewSetMixin

from rdmo.conditions.models import Condition
from rdmo.core.permissions import HasModelPermission
from rdmo.core.utils import human2bytes, return_file_response
from rdmo.options.models import OptionSet
from rdmo.questions.models import Page, Question, QuestionSet
from rdmo.tasks.models import Task
from rdmo.views.models import View

from .filters import SnapshotFilterBackend, ValueFilterBackend
from .models import Continuation, Integration, Invite, Issue, Membership, Project, Snapshot, Value
from .permissions import HasProjectPagePermission, HasProjectPermission, HasProjectsPermission
from .serializers.v1 import (
    IntegrationSerializer,
    InviteSerializer,
    IssueSerializer,
    MembershipSerializer,
    ProjectIntegrationSerializer,
    ProjectInviteSerializer,
    ProjectInviteUpdateSerializer,
    ProjectIssueSerializer,
    ProjectMembershipSerializer,
    ProjectMembershipUpdateSerializer,
    ProjectSerializer,
    ProjectSnapshotSerializer,
    ProjectValueSerializer,
    SnapshotSerializer,
    ValueSerializer,
)
from .serializers.v1.overview import ProjectOverviewSerializer
from .serializers.v1.page import PageSerializer
from .utils import check_conditions, send_invite_email


class ProjectViewSet(ModelViewSet):
    permission_classes = (HasModelPermission | HasProjectsPermission, )
    serializer_class = ProjectSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'title',
        'user',
        'user__username',
        'catalog',
        'catalog__uri'
    )

    def get_queryset(self):
        return Project.objects.filter_user(self.request.user).select_related('catalog')

    @action(detail=True, permission_classes=(IsAuthenticated, ))
    def overview(self, request, pk=None):
        project = self.get_object()

        # prefetch only the pages (and their conditions)
        prefetch_related_objects([project.catalog],
                                 'catalog_sections__section__section_pages__page__conditions')

        serializer = ProjectOverviewSerializer(project, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, permission_classes=(HasModelPermission | HasProjectPermission, ))
    def resolve(self, request, pk=None):
        snapshot_id = request.GET.get('snapshot')
        set_prefix = request.GET.get('set_prefix')
        set_index = request.GET.get('set_index')

        values = self.get_object().values.filter(snapshot_id=snapshot_id).select_related('attribute', 'option')

        page_id = request.GET.get('page')
        if page_id:
            try:
                page = Page.objects.get(id=page_id)
                conditions = page.conditions.select_related('source', 'target_option')
                if check_conditions(conditions, values, set_prefix, set_index):
                    return Response({'result': True})
            except Page.DoesNotExist:
                pass

        questionset_id = request.GET.get('questionset')
        if questionset_id:
            try:
                questionset = QuestionSet.objects.get(id=questionset_id)
                conditions = questionset.conditions.select_related('source', 'target_option')
                if check_conditions(conditions, values, set_prefix, set_index):
                    return Response({'result': True})
            except QuestionSet.DoesNotExist:
                pass

        question_id = request.GET.get('question')
        if question_id:
            try:
                question = Question.objects.get(id=question_id)
                conditions = question.conditions.select_related('source', 'target_option')
                if check_conditions(conditions, values, set_prefix, set_index):
                    return Response({'result': True})
            except Question.DoesNotExist:
                pass

        optionset_id = request.GET.get('optionset')
        if optionset_id:
            try:
                optionset = OptionSet.objects.get(id=optionset_id)
                conditions = optionset.conditions.select_related('source', 'target_option')
                if check_conditions(conditions, values, set_prefix, set_index):
                    return Response({'result': True})
            except OptionSet.DoesNotExist:
                pass

        condition_id = request.GET.get('condition')
        if condition_id:
            try:
                condition = Condition.objects.select_related('source', 'target_option').get(id=condition_id)
                if check_conditions([condition], values, set_prefix, set_index):
                    return Response({'result': True})
            except Condition.DoesNotExist:
                pass

        return Response({'result': False})

    @action(detail=True, permission_classes=(HasModelPermission | HasProjectPermission, ))
    def options(self, request, pk=None):
        project = self.get_object()

        try:
            try:
                optionset_id = request.GET.get('optionset')
                optionset = OptionSet.objects.get(pk=optionset_id)
            except (ValueError, OptionSet.DoesNotExist) as e:
                raise NotFound() from e

            # check if the optionset belongs to this catalog and if it has a provider
            if Question.objects.filter_by_catalog(project.catalog).filter(optionsets=optionset) and \
                    optionset.provider is not None:
                options = optionset.provider.get_options(project, search=request.GET.get('search'))
                return Response(options)

        except OptionSet.DoesNotExist:
            pass

        # if it didn't work return 404
        raise NotFound()

    @action(detail=True, permission_classes=(IsAuthenticated, ))
    def progress(self, request, pk=None):
        project = self.get_object()
        project.catalog.prefetch_elements()
        return Response(project.progress)

    def perform_create(self, serializer):
        project = serializer.save(site=get_current_site(self.request))

        # add all tasks to project
        tasks = Task.objects.filter_current_site() \
                            .filter_catalog(project.catalog) \
                            .filter_group(self.request.user) \
                            .filter_availability(self.request.user)
        for task in tasks:
            project.tasks.add(task)

        if self.request.data.get('views') is None:
            # add all views to project
            views = View.objects.filter_current_site() \
                                .filter_catalog(project.catalog) \
                                .filter_group(self.request.user) \
                                .filter_availability(self.request.user)
            for view in views:
                project.views.add(view)

        # add current user as owner
        membership = Membership(project=project, user=self.request.user, role='owner')
        membership.save()


class ProjectNestedViewSetMixin(NestedViewSetMixin):

    def initial(self, request, *args, **kwargs):
        self.project = self.get_project_from_parent_viewset()
        super().initial(request, *args, **kwargs)

    def get_project_from_parent_viewset(self):
        try:
            return Project.objects.filter_user(self.request.user).get(pk=self.get_parents_query_dict().get('project'))
        except Project.DoesNotExist as e:
            raise Http404 from e

    def perform_create(self, serializer):
        # this call provides the nested serializers with the project
        serializer.save(project=self.project)


class ProjectMembershipViewSet(ProjectNestedViewSetMixin, ModelViewSet):
    permission_classes = (HasModelPermission | HasProjectPermission, )

    filter_backends = (DjangoFilterBackend, )
    filterset_fields = (
        'user',
        'user__username',
        'role'
    )

    def get_queryset(self):
        try:
            return Membership.objects.filter(project=self.project)
        except AttributeError:
            # this is needed for the swagger ui
            return Membership.objects.none()

    def get_serializer_class(self):
        if self.action == 'update':
            return ProjectMembershipUpdateSerializer
        else:
            return ProjectMembershipSerializer


class ProjectIntegrationViewSet(ProjectNestedViewSetMixin, ModelViewSet):
    permission_classes = (HasModelPermission | HasProjectPermission, )
    serializer_class = ProjectIntegrationSerializer

    filter_backends = (DjangoFilterBackend, )
    filterset_fields = (
        'provider_key',
    )

    def get_queryset(self):
        try:
            return Integration.objects.filter(project=self.project)
        except AttributeError:
            # this is needed for the swagger ui
            return Integration.objects.none()


class ProjectInviteViewSet(ProjectNestedViewSetMixin, ModelViewSet):
    permission_classes = (HasModelPermission | HasProjectPermission, )

    filter_backends = (DjangoFilterBackend, )
    filterset_fields = (
        'user',
        'user__username',
        'email',
        'role'
    )

    def get_queryset(self):
        try:
            return Invite.objects.filter(project=self.project)
        except AttributeError:
            # this is needed for the swagger ui
            return Invite.objects.none()

    def get_serializer_class(self):
        if self.action == 'update':
            return ProjectInviteUpdateSerializer
        else:
            return ProjectInviteSerializer

    def perform_create(self, serializer):
        super().perform_create(serializer)
        if settings.PROJECT_SEND_INVITE:
            send_invite_email(self.request, serializer.instance)


class ProjectIssueViewSet(ProjectNestedViewSetMixin, ListModelMixin, RetrieveModelMixin,
                          UpdateModelMixin, GenericViewSet):
    permission_classes = (HasModelPermission | HasProjectPermission, )
    serializer_class = ProjectIssueSerializer

    filter_backends = (DjangoFilterBackend, )
    filterset_fields = (
        'task',
        'task__uri',
        'status'
    )

    def get_queryset(self):
        try:
            return Issue.objects.filter(project=self.project).prefetch_related('resources')
        except AttributeError:
            # this is needed for the swagger ui
            return Issue.objects.none()


class ProjectSnapshotViewSet(ProjectNestedViewSetMixin, CreateModelMixin, RetrieveModelMixin,
                             UpdateModelMixin, ListModelMixin, GenericViewSet):
    permission_classes = (HasModelPermission | HasProjectPermission, )
    serializer_class = ProjectSnapshotSerializer

    def get_queryset(self):
        try:
            return self.project.snapshots.all()
        except AttributeError:
            # this is needed for the swagger ui
            return Snapshot.objects.none()


class ProjectValueViewSet(ProjectNestedViewSetMixin, ModelViewSet):
    permission_classes = (HasModelPermission | HasProjectPermission, )
    serializer_class = ProjectValueSerializer

    filter_backends = (ValueFilterBackend, DjangoFilterBackend)
    filterset_fields = (
        # attribute is part of ValueFilterBackend
        'attribute__uri',
        'option',
        'option__uri',
    )

    def get_queryset(self):
        try:
            return self.project.values.filter(snapshot=None).select_related('attribute', 'option')
        except AttributeError:
            # this is needed for the swagger ui
            return Value.objects.none()

    @action(detail=True, methods=['DELETE'],
            permission_classes=(HasModelPermission | HasProjectPermission, ))
    def set(self, request, parent_lookup_project, pk=None):
        # delete all values for questions in questionset collections with the attribute
        # for this value and the same set_prefix and set_index
        value = self.get_object()
        value.delete()

        # prefetch most elements of the catalog
        self.project.catalog.prefetch_elements()

        # collect the attributes of all questions of all pages or questionsets
        # of this catalog, which have the attribute of this value
        attributes = set()
        elements = self.project.catalog.pages + self.project.catalog.questions
        for element in elements:
            if element.attribute == value.attribute:
                attributes.update([descendant.attribute for descendant in element.descendants])

        values = self.get_queryset().filter(attribute__in=attributes, set_prefix=value.set_prefix,
                                            set_index=value.set_index)
        values.delete()

        return Response(status=204)

    @action(detail=True, methods=['GET', 'POST'],
            permission_classes=(HasModelPermission | HasProjectPermission, ))
    def file(self, request, parent_lookup_project, pk=None):
        value = self.get_object()

        if request.method == 'POST':
            value.file = request.FILES.get('file')

            # check if the project is reached
            if value.file and value.file.size + value.project.file_size > human2bytes(settings.PROJECT_FILE_QUOTA):
                raise serializers.ValidationError({
                    'value': [_('You reached the file quota for this project.')]
                })

            value.save()
            serializer = self.get_serializer(value)
            return Response(serializer.data)

        else:
            if value.file:
                return return_file_response(value.file.name, value.file_type)

        # if it didn't work return 404
        raise NotFound()


class ProjectPageViewSet(ProjectNestedViewSetMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = (HasModelPermission | HasProjectPagePermission, )
    serializer_class = PageSerializer

    def get_queryset(self):
        try:
            self.project.catalog.prefetch_elements()
            page = Page.objects.filter_by_catalog(self.project.catalog).prefetch_related(
                *Page.prefetch_lookups,
                'page_questions__question__optionsets__optionset_options__option',
                'page_questionsets__questionset__questionset_questions__question__optionsets__optionset_options__option',
            )
            return page
        except AttributeError:
            # this is needed for the swagger ui
            return Page.objects.none()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['catalog'] = self.project.catalog
        return context

    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        if response.status_code == 200 and kwargs.get('pk'):
            try:
                continuation = Continuation.objects.get(project=self.project, user=self.request.user)
            except Continuation.DoesNotExist:
                continuation = Continuation(project=self.project, user=self.request.user)

            continuation.page_id = kwargs.get('pk')
            continuation.save()

        return response

    def retrieve(self, request, *args, **kwargs):
        page = self.get_object()
        conditions = page.conditions.select_related('source', 'target_option')

        values = self.project.values.filter(snapshot=None).select_related('attribute', 'option')

        if check_conditions(conditions, values):
            serializer = self.get_serializer(page)
            return Response(serializer.data)
        else:
            if request.GET.get('back') == 'true':
                prev_page = self.project.catalog.get_prev_page(page)
                if prev_page is not None:
                    url = reverse('v1-projects:project-page-detail',
                                  args=[self.project.id, prev_page.id]) + '?back=true'
                    return HttpResponseRedirect(url, status=303)
            else:
                next_page = self.project.catalog.get_next_page(page)
                if next_page is not None:
                    url = reverse('v1-projects:project-page-detail', args=[self.project.id, next_page.id])
                    return HttpResponseRedirect(url, status=303)

            # indicate end of catalog
            return Response(status=204)

    @action(detail=False, url_path='continue', permission_classes=(HasModelPermission | HasProjectPagePermission, ))
    def get_continue(self, request, pk=None, parent_lookup_project=None):
        try:
            continuation = Continuation.objects.get(project=self.project, user=self.request.user)

            try:
                page = Page.objects.filter_by_catalog(self.project.catalog).get(id=continuation.page_id)
            except Page.DoesNotExist:
                page = self.project.catalog.pages[0]

        except Continuation.DoesNotExist:
            page = self.project.catalog.pages[0]

        serializer = self.get_serializer(page)
        return Response(serializer.data)


class MembershipViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission | HasProjectsPermission, )
    serializer_class = MembershipSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'user',
        'user__username',
        'role'
    )

    def get_queryset(self):
        return Membership.objects.filter_user(self.request.user)


class IntegrationViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission | HasProjectsPermission, )
    serializer_class = IntegrationSerializer

    filter_backends = (DjangoFilterBackend, )
    filterset_fields = (
        'project',
        'provider_key'
    )

    def get_queryset(self):
        return Integration.objects.filter_user(self.request.user)


class InviteViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission | HasProjectsPermission, )
    serializer_class = InviteSerializer

    filter_backends = (DjangoFilterBackend, )
    filterset_fields = (
        'user',
        'user__username',
        'email',
        'role'
    )

    def get_queryset(self):
        return Invite.objects.filter_user(self.request.user)

    def get_detail_permission_object(self, obj):
        return obj.project


class IssueViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission | HasProjectsPermission, )
    serializer_class = IssueSerializer

    filter_backends = (DjangoFilterBackend, )
    filterset_fields = (
        'task',
        'task__uri',
        'status'
    )

    def get_queryset(self):
        return Issue.objects.filter_user(self.request.user).prefetch_related('resources')


class SnapshotViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission | HasProjectsPermission, )
    serializer_class = SnapshotSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'title',
        'project'
    )

    def get_queryset(self):
        return Snapshot.objects.filter_user(self.request.user)


class ValueViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission | HasProjectsPermission, )
    serializer_class = ValueSerializer

    filter_backends = (SnapshotFilterBackend, DjangoFilterBackend)
    filterset_fields = (
        'project',
        # snapshot is part of SnapshotFilterBackend
        'attribute',
        'attribute__uri',
        'option',
        'option__uri',
    )

    def get_queryset(self):
        return Value.objects.filter_user(self.request.user).select_related('attribute', 'option')

    @action(detail=True, permission_classes=(HasModelPermission | HasProjectsPermission, ))
    def file(self, request, pk=None):
        value = self.get_object()

        if value.file:
            return return_file_response(value.file.name, value.file_type)

        # if it didn't work return 404
        raise NotFound()
