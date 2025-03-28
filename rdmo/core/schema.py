

from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view


def filter_endpoints(endpoints):
    for (path, path_regex, method, callback) in endpoints:
        if not path.startswith((
            '/api/v1/management/',
            '/api/v1/overlays/'
        )):
            yield (path, path_regex, method, callback)



class ViewExtension(OpenApiViewExtension):

    def view_replacement(self):
        # create the replaced class using type to assign the name dynamically (for errors/warnings)
        replaced_class_name = f'Fixed{self.target_class.__name__}'
        replaced_class = type(replaced_class_name, (self.target_class,), {})

        # optionally, patch the get_queryset method
        self.patch_get_queryset_with_try_except(replaced_class)

        # apply the decorator and return
        extend_schema_view(**self.get_extend_schema_view_args())(replaced_class)
        return replaced_class

    def get_extend_schema_view_args(self):
        return {
            action: extend_schema(**self.get_extend_schema_args(action))
            for action in self.actions
        }

    def get_extend_schema_args(self, action):
        return {}

    def patch_get_queryset_with_try_except(self, cls):
        def get_queryset(self):
            try:
                return super(cls, self).get_queryset()
            except AttributeError as e:
                # fallback for drf-spectacular (e.g., self.project or self.request.user not set)
                serializer_class = self.get_serializer_class()
                model = getattr(getattr(serializer_class, 'Meta', None), 'model', None)
                if model and hasattr(model, 'objects'):
                    return model.objects.none()
                # unexpected error
                raise e from e

        cls.get_queryset = get_queryset


class ModelViewSetMixin:

    actions = [
        'list',
        'create',
        'retrieve',
        'update',
        'partial_update',
        'destroy'
    ]


class ReadOnlyModelViewSetMixin:

    actions = [
        'list',
        'retrieve',
    ]


class ExportViewSetMixin:

    actions = [
        'export',
        'detail_export'
    ]


class ParentLookupIdMixin:

    def get_extend_schema_args(self, action):
        return {
            'parameters': [
                OpenApiParameter('parent_lookup_project', int, OpenApiParameter.PATH)
            ]
        }


class OperationIdMixin:

    def get_extend_schema_args(self, action):
        return {
            'operation_id': self.operation_id_template.format(action)
        }


class KeyValueMixin:

    def get_extend_schema_view_args(self):
        return {
            'list': extend_schema(responses={
                200: {
                    "type": "object",
                    "example": {
                        "key1": "value1",
                        "key2": "value2",
                        "key3": "value3",
                    }
                }
            })
        }


class ConditionViewSetExtension(OperationIdMixin, ExportViewSetMixin, ViewExtension):
    target_class = 'rdmo.conditions.viewsets.ConditionViewSet'
    operation_id_template = 'conditions_conditions_{}'


class AttributeViewSetExtension(OperationIdMixin, ExportViewSetMixin, ViewExtension):
    target_class = 'rdmo.domain.viewsets.AttributeViewSet'
    operation_id_template = 'domain_attributes_{}'


class SettingsViewSetExtension(KeyValueMixin, ViewExtension):
    target_class = 'rdmo.core.viewsets.SettingsViewSet'


class TemplatesViewSetExtension(KeyValueMixin, ViewExtension):
    target_class = 'rdmo.core.viewsets.TemplatesViewSet'


class OptionSetViewSetExtension(OperationIdMixin, ExportViewSetMixin, ViewExtension):
    target_class = 'rdmo.options.viewsets.OptionSetViewSet'
    operation_id_template = 'options_optionsets_{}'


class OptionViewSetExtension(OperationIdMixin, ExportViewSetMixin, ViewExtension):
    target_class = 'rdmo.options.viewsets.OptionViewSet'
    operation_id_template = 'options_options_{}'


class ProjectIntegrationViewSetExtension(ParentLookupIdMixin, ModelViewSetMixin, ViewExtension):
    target_class = 'rdmo.projects.viewsets.ProjectIntegrationViewSet'


class ProjectInviteViewSetExtension(ParentLookupIdMixin, ModelViewSetMixin, ViewExtension):
    target_class = 'rdmo.projects.viewsets.ProjectInviteViewSet'


class ProjectIssueViewSetExtension(ParentLookupIdMixin, ViewExtension):
    target_class = 'rdmo.projects.viewsets.ProjectIssueViewSet'
    actions = ['list', 'retrieve', 'update', 'partial_update']


class ProjectMembershipViewSetExtension(ParentLookupIdMixin, ModelViewSetMixin, ViewExtension):
    target_class = 'rdmo.projects.viewsets.ProjectMembershipViewSet'


class ProjectPageViewSetExtension(ParentLookupIdMixin, ViewExtension):
    target_class = 'rdmo.projects.viewsets.ProjectPageViewSet'
    actions = ['retrieve', 'get_continue']


class ProjectSnapshotViewSetExtension(ParentLookupIdMixin, ViewExtension):
    target_class = 'rdmo.projects.viewsets.ProjectSnapshotViewSet'
    actions = ['list', 'create', 'retrieve', 'update', 'partial_update']


class ProjectValueViewSetExtension(ParentLookupIdMixin, ModelViewSetMixin, ViewExtension):
    target_class = 'rdmo.projects.viewsets.ProjectValueViewSet'
    actions = [*ModelViewSetMixin.actions, 'copy_set', 'delete_set', 'file']


class MembershipViewSetExtension(ReadOnlyModelViewSetMixin, ViewExtension):
    target_class = 'rdmo.projects.viewsets.MembershipViewSet'
    operation_id_template = 'projects_membership_{}'


class CatalogViewSetExtension(OperationIdMixin, ExportViewSetMixin, ViewExtension):
    target_class = 'rdmo.questions.viewsets.CatalogViewSet'
    operation_id_template = 'questions_catalog_{}'


class SectionViewSetExtension(OperationIdMixin, ExportViewSetMixin, ViewExtension):
    target_class = 'rdmo.questions.viewsets.SectionViewSet'
    operation_id_template = 'questions_section_{}'


class PageViewSetExtension(OperationIdMixin, ExportViewSetMixin, ViewExtension):
    target_class = 'rdmo.questions.viewsets.PageViewSet'
    operation_id_template = 'questions_page_{}'


class QuestionSetViewSetExtension(OperationIdMixin, ExportViewSetMixin, ViewExtension):
    target_class = 'rdmo.questions.viewsets.QuestionSetViewSet'
    operation_id_template = 'questions_questionset_{}'


class QuestionViewSetExtension(OperationIdMixin, ExportViewSetMixin, ViewExtension):
    target_class = 'rdmo.questions.viewsets.QuestionViewSet'
    operation_id_template = 'questions_questions_{}'


class TaskViewSetExtension(OperationIdMixin, ExportViewSetMixin, ViewExtension):
    target_class = 'rdmo.tasks.viewsets.TaskViewSet'
    operation_id_template = 'tasks_tasks_{}'


class ViewViewSetExtension(OperationIdMixin, ExportViewSetMixin, ViewExtension):
    target_class = 'rdmo.views.viewsets.ViewViewSet'
    operation_id_template = 'views_views_{}'
