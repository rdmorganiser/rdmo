from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import OuterRef, Prefetch, Q, Subquery
from django.db.models.functions import Coalesce, Greatest
from django.http import Http404, HttpResponseRedirect
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.serializers import ValidationError
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_extensions.mixins import NestedViewSetMixin

from rdmo.conditions.models import Condition
from rdmo.core.permissions import HasModelPermission
from rdmo.core.utils import human2bytes, is_truthy, return_file_response
from rdmo.options.models import OptionSet
from rdmo.questions.models import Catalog, Page, Question, QuestionSet
from rdmo.tasks.models import Task
from rdmo.views.models import View

from .filters import (
    ProjectDateFilterBackend,
    ProjectOrderingFilter,
    ProjectSearchFilterBackend,
    ProjectUserFilterBackend,
    SnapshotFilterBackend,
    ValueFilterBackend,
)
from .models import Continuation, Integration, Invite, Issue, Membership, Project, Snapshot, Value, Visibility
from .permissions import (
    HasProjectPagePermission,
    HasProjectPermission,
    HasProjectProgressModelPermission,
    HasProjectProgressObjectPermission,
    HasProjectsPermission,
    HasProjectVisibilityModelPermission,
    HasProjectVisibilityObjectPermission,
)
from .progress import (
    compute_navigation,
    compute_next_relevant_page,
    compute_progress,
    compute_sets,
    compute_show_page,
    resolve_conditions,
)
from .serializers.v1 import (
    IntegrationSerializer,
    InviteSerializer,
    IssueSerializer,
    MembershipSerializer,
    ProjectCopySerializer,
    ProjectIntegrationSerializer,
    ProjectInviteSerializer,
    ProjectInviteUpdateSerializer,
    ProjectIssueSerializer,
    ProjectMembershipSerializer,
    ProjectMembershipUpdateSerializer,
    ProjectSerializer,
    ProjectSnapshotSerializer,
    ProjectValueSerializer,
    ProjectVisibilitySerializer,
    SnapshotSerializer,
    UserInviteSerializer,
    ValueSearchSerializer,
    ValueSerializer,
)
from .serializers.v1.overview import CatalogSerializer, ProjectOverviewSerializer
from .serializers.v1.page import PageSerializer
from .utils import (
    check_conditions,
    compute_set_prefix_from_set_value,
    copy_project,
    get_contact_message,
    get_upload_accept,
    send_contact_message,
    send_invite_email,
)


class ProjectPagination(PageNumberPagination):
    page_size = settings.PROJECT_TABLE_PAGE_SIZE


class ProjectViewSet(ModelViewSet):
    permission_classes = (HasModelPermission | HasProjectsPermission, )
    serializer_class = ProjectSerializer
    pagination_class = ProjectPagination

    filter_backends = (
        DjangoFilterBackend,
        ProjectUserFilterBackend,
        ProjectDateFilterBackend,
        ProjectOrderingFilter,
        ProjectSearchFilterBackend,
    )
    filterset_fields = (
        'title',
        # user is part of ProjectUserFilterBackend
        'catalog',
        'catalog__uri'
    )
    ordering_fields = (
        'title',
        'progress',
        'role',
        'owner',
        'updated',
        'created',
        'last_changed'
    )

    def get_queryset(self):
        queryset = Project.objects.filter_user(self.request.user).distinct().prefetch_related(
            'snapshots',
            'views',
            Prefetch('memberships', queryset=Membership.objects.select_related('user'), to_attr='memberships_list')
        ).select_related('catalog', 'visibility')

        # prepare subquery for last_changed
        last_changed_subquery = Subquery(
            Value.objects.filter(project=OuterRef('pk')).order_by('-updated').values('updated')[:1]
        )
        # the 'updated' field from a Project always returns a valid DateTime value
        # when Greatest returns null, then Coalesce will return the value for 'updated' as a fall-back
        # when Greatest returns a value, then Coalesce will return this value
        queryset = queryset.annotate(last_changed=Coalesce(Greatest(last_changed_subquery, 'updated'), 'updated'))

        return queryset

    @action(detail=True, methods=['POST'],
            permission_classes=(HasModelPermission | HasProjectPermission, ))
    def copy(self, request, pk=None):
        instance = self.get_object()
        serializer = ProjectCopySerializer(instance, data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)

        # update instance
        for key, value in serializer.validated_data.items():
            setattr(instance, key, value)

        site = get_current_site(self.request)
        owners = [self.request.user]
        project_copy = copy_project(instance, site, owners)

        serializer = self.get_serializer(project_copy)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, permission_classes=(HasModelPermission | HasProjectPermission, ))
    def overview(self, request, pk=None):
        project = self.get_object()
        serializer = ProjectOverviewSerializer(project, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, url_path=r'navigation(/(?P<section_id>\d+))?',
            permission_classes=(HasModelPermission | HasProjectPermission, ))
    def navigation(self, request, pk=None, section_id=None):
        project = self.get_object()

        section = None
        if section_id is not None:
            try:
                section = project.catalog.sections.get(pk=section_id)
            except ObjectDoesNotExist as e:
                raise NotFound() from e

        project.catalog.prefetch_elements()

        navigation = compute_navigation(section, project)
        return Response(navigation)

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
            project.catalog.prefetch_elements()
            if Question.objects.filter_by_catalog(project.catalog).filter(optionsets=optionset) and \
                    optionset.provider is not None:
                options = []
                for option in optionset.provider.get_options(project, search=request.GET.get('search'),
                                                             user=request.user, site=request.site):
                    if 'id' not in option:
                        raise RuntimeError(f"'id' is missing in options of '{optionset.provider.class_name}'")
                    elif 'text' not in option:
                        raise RuntimeError(f"'text' is missing in options of '{optionset.provider.class_name}'")
                    if 'text_and_help' not in option:
                        if 'help' in option:
                            option['text_and_help'] = '{text} [{help}]'.format(**option)
                        else:
                            option['text_and_help'] = '{text}'.format(**option)
                    options.append(option)

                return Response(options)

        except OptionSet.DoesNotExist:
            pass

        # if it didn't work return 404
        raise NotFound()

    @action(detail=True, methods=['get', 'post'],
            permission_classes=(HasProjectProgressModelPermission | HasProjectProgressObjectPermission, ))
    def progress(self, request, pk=None):
        project = self.get_object()

        if request.method == 'POST' or project.progress_count is None or project.progress_total is None:
            # compute the progress, but store it only, if it has changed
            project.catalog.prefetch_elements()
            progress_count, progress_total = compute_progress(project)
            if progress_count != project.progress_count or progress_total != project.progress_total:
                project.progress_count, project.progress_total = progress_count, progress_total
                project.save()
        try:
            ratio = project.progress_count / project.progress_total
        except ZeroDivisionError:
            ratio = 0

        return Response({
            'count': project.progress_count,
            'total': project.progress_total,
            'ratio': ratio
        })

    @action(detail=True, methods=['get', 'post', 'delete'],
            permission_classes=(HasProjectVisibilityModelPermission | HasProjectVisibilityObjectPermission, ))
    def visibility(self, request, pk=None):
        project = self.get_object()

        try:
            instance = project.visibility
        except Visibility.DoesNotExist:
            instance = None

        serializer = ProjectVisibilitySerializer(instance)

        if request.method == 'POST':
            serializer = ProjectVisibilitySerializer(instance, data=dict(**request.data, project=project.id))
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        elif request.method == 'DELETE':
            if instance is not None:
                instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            if instance is not None:
                serializer = ProjectVisibilitySerializer(instance)
                return Response(serializer.data)

        # if nothing worked, raise 404
        raise Http404

    @action(detail=True, methods=['get', 'post'],
            permission_classes=(HasModelPermission | HasProjectPermission, ))
    def contact(self, request, pk):
        if settings.PROJECT_CONTACT:
            project = self.get_object()
            if request.method == 'POST':
                subject = request.data.get('subject')
                message = request.data.get('message')

                if subject and message:
                    send_contact_message(request, subject, message)
                    return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    raise ValidationError({
                        'subject': [_('This field may not be blank.')] if not subject else [],
                        'message': [_('This field may not be blank.')] if not message else []
                    })
            else:
                project.catalog.prefetch_elements()
                return Response(get_contact_message(request, project))
        else:
            raise Http404

    @action(detail=False, url_path='upload-accept', permission_classes=(IsAuthenticated, ))
    def upload_accept(self, request):
        return Response(get_upload_accept())

    @action(detail=False, permission_classes=(IsAuthenticated, ))
    def imports(self, request):
        return Response([{
            'key': key,
            'label': label,
            'class_name': class_name,
            'href': reverse('project_create_import', args=[key])
        } for key, label, class_name in settings.PROJECT_IMPORTS if key in settings.PROJECT_IMPORTS_LIST] )

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

    @action(detail=False, methods=['POST'], url_path='set',
            permission_classes=(HasModelPermission | HasProjectPermission, ))
    def copy_set(self, request, parent_lookup_project, pk=None):
        # copy all values for questions in questionset collections with the attribute
        # for this value and the same set_prefix and set_index

        # obtain the id of the set value for the set we want to copy
        try:
            copy_value_id = int(request.data.pop('copy_set_value'))
        except KeyError as e:
            raise ValidationError({
                'copy_set_value': [_('This field may not be blank.')]
            }) from e
        except ValueError as e:
            raise NotFound from e

        # look for this value in the database, using the users permissions, and
        # collect all values for this set and all descendants
        try:
            copy_value = Value.objects.filter_user(self.request.user).get(id=copy_value_id)
            copy_values = Value.objects.filter_user(self.request.user).filter_set(copy_value)
        except Value.DoesNotExist as e:
            raise NotFound from e

        # init list of values to return
        response_values = []

        set_value_id = request.data.get('id')
        if set_value_id:
            # if an id is given in the post request, this is an import
            try:
                # look for the set value for the set we want to import into
                set_value = Value.objects.filter_user(self.request.user).get(id=set_value_id)

                # collect all non-empty values for this set and all descendants and convert
                # them to a list to compare them later to the new values
                set_values = Value.objects.filter_user(self.request.user).filter_set(set_value)
                set_values_list = set_values.exclude_empty().values_list('attribute', 'set_prefix', 'set_index')
                set_empty_values_list = set_values.filter_empty().values_list(
                    'attribute', 'set_prefix', 'set_index', 'collection_index'
                )
            except Value.DoesNotExist as e:
                raise NotFound from e
        else:
            # otherwise, we want to create a new set and need to create a new set value
            # de-serialize the posted new set value and save it, use the ValueSerializer
            # instead of ProjectValueSerializer, since the latter does not include project
            set_value_serializer = ValueSerializer(data={
                'project': parent_lookup_project,
                **request.data
            })
            set_value_serializer.is_valid(raise_exception=True)
            set_value = set_value_serializer.save()
            set_values_list = set_empty_values_list = []

            # add the new set value to response_values
            response_values.append(set_value_serializer.data)

        # create new values for the new set
        new_values = []
        updated_values = []
        for value in copy_values:
            value.id = None
            value.project = set_value.project
            value.snapshot = None
            if value.set_prefix == set_value.set_prefix:
                value.set_index = set_value.set_index
            else:
                value.set_prefix = compute_set_prefix_from_set_value(set_value, value)

            # check if the value already exists, we do not consider collection_index
            # since we do not want to import e.g. into partially filled checkboxes
            if (value.attribute_id, value.set_prefix, value.set_index) in set_values_list:
                # do not overwrite existing values
                pass
            elif (value.attribute_id, value.set_prefix,
                  value.set_index, value.collection_index) in set_empty_values_list:
                # update empty values
                updated_value = set_values.get(attribute_id=value.attribute_id, set_prefix=value.set_prefix,
                                                set_index=value.set_index, collection_index=value.collection_index)
                updated_value.text = value.text
                updated_value.option = value.option
                updated_value.external_id = value.external_id
                updated_value.save()

                updated_values.append(updated_value)
            else:
                new_values.append(value)

        # bulk create the new values
        created_values = Value.objects.bulk_create(new_values)
        response_values += [ValueSerializer(instance=value).data for value in created_values]
        response_values += [ValueSerializer(instance=value).data for value in updated_values]

        # return all new values
        return Response(response_values, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['DELETE'], url_path='set',
            permission_classes=(HasModelPermission | HasProjectPermission, ))
    def delete_set(self, request, parent_lookup_project, pk=None):
        # delete all values for questions in questionset collections with the attribute
        # for this value and the same set_prefix and set_index
        set_value = self.get_object()
        set_value.delete()

        # collect all values for this set and all descendants and delete them
        values = self.get_queryset().filter_set(set_value)
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
        catalog = self.project.catalog
        values = self.project.values.filter(snapshot=None).select_related('attribute', 'option')

        sets = compute_sets(values)
        resolved_conditions = resolve_conditions(catalog, values, sets)

        # check if the current page meets conditions
        if compute_show_page(page, resolved_conditions):
            serializer = self.get_serializer(page)
            return Response(serializer.data)
        else:
            # determine the direction of navigation (previous or next)
            direction = 'prev' if is_truthy(request.GET.get('back')) else 'next'

            # find the next relevant page with from pages and resolved conditions
            next_relevant_page = compute_next_relevant_page(page, direction, catalog, resolved_conditions)

            if next_relevant_page is not None:
                url = reverse('v1-projects:project-page-detail', args=[self.project.id, next_relevant_page.id])
                return HttpResponseRedirect(url, status=303)

            # end of catalog, if no next relevant page is found
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

    @action(detail=False, permission_classes=(IsAuthenticated, ))
    def user(self, request):
        invites = Invite.objects.filter(user=self.request.user)
        serializer = UserInviteSerializer(invites, many=True)
        return Response(serializer.data)

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

    filter_backends = (SnapshotFilterBackend, DjangoFilterBackend, SearchFilter)
    filterset_fields = (
        'project',
        # snapshot is part of SnapshotFilterBackend
        'attribute',
        'attribute__uri',
        'attribute__path',
        'option',
        'option__uri',
        'option__uri_path'
    )

    search_fields = ['text', 'project__title', 'snapshot__title']

    def get_queryset(self):
        return Value.objects.filter_user(self.request.user).select_related('attribute', 'option')

    @action(detail=False, permission_classes=(HasModelPermission | HasProjectsPermission, ))
    def search(self, request):
        queryset = self.filter_queryset(self.get_queryset()).exclude_empty().select_related('project', 'snapshot')

        if is_truthy(request.GET.get('collection')):
            # if collection is set (for checkboxes), we first select each distinct set and create a Q object with it
            # by doing so we can select an undetermined number of values which belong to an exact number of sets
            # given by settings.PROJECT_VALUES_SEARCH_LIMIT
            values_list = queryset.order_by('project_id', 'snapshot_id', 'attribute_id', 'set_prefix', 'set_index') \
                                  .distinct('project_id', 'snapshot_id', 'attribute_id', 'set_prefix', 'set_index') \
                                  .values('project_id', 'snapshot_id', 'attribute_id', 'set_prefix', 'set_index') \
                                  [:settings.PROJECT_VALUES_SEARCH_LIMIT]

            q = Q()
            for values_dict in values_list:
                q |= Q(**values_dict)

            queryset = queryset.filter(q)
        else:
            queryset = queryset[:settings.PROJECT_VALUES_SEARCH_LIMIT]

        serializer = ValueSearchSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, permission_classes=(HasModelPermission | HasProjectsPermission, ))
    def file(self, request, pk=None):
        value = self.get_object()

        if value.file:
            return return_file_response(value.file.name, value.file_type)

        # if it didn't work return 404
        raise NotFound()


class CatalogViewSet(ListModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated, )

    serializer_class = CatalogSerializer

    def get_queryset(self):
        return Catalog.objects.filter_current_site() \
                              .filter_group(self.request.user) \
                              .order_by('-available', 'order')
