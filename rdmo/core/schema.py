import ast
import inspect
import textwrap

from django.db.models.query import QuerySet

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
        replaced_class = self._create_replacement_class()

        if self._should_patch_get_queryset():
            self._patch_get_queryset(replaced_class)

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

    def _create_replacement_class(self):
        replaced_class_name = f'Fixed{self.target_class.__name__}'
        return type(replaced_class_name, (self.target_class,), {})

    def _should_patch_get_queryset(self):
        return hasattr(self.target_class, 'get_queryset') and self._uses_request_user(self.target_class)

    def _patch_get_queryset(self, cls):
        def get_fallback_queryset(self):
            try:
                serializer_class = getattr(self, 'serializer_class', None)
                model = getattr(getattr(serializer_class, 'Meta', None), 'model', None)
                if model and hasattr(model, 'objects'):
                    return model.objects.none()
            except Exception:
                pass
            return QuerySet().none()

        def patched_get_queryset(self):
            return self.get_fallback_queryset()

        cls.get_fallback_queryset = get_fallback_queryset
        cls.get_queryset = patched_get_queryset

    def _uses_request_user(self, cls):
        try:
            source = inspect.getsource(cls.get_queryset)
            source = textwrap.dedent(source)
            parsed = ast.parse(source)

            class RequestUserVisitor(ast.NodeVisitor):
                def __init__(self):
                    self.found = False

                def visit_Attribute(self, node):
                    if (
                        isinstance(node.value, ast.Attribute) and
                        isinstance(node.value.value, ast.Name) and
                        node.value.value.id == 'self' and
                        node.value.attr == 'request' and
                        node.attr == 'user'
                    ):
                        self.found = True
                    self.generic_visit(node)

            visitor = RequestUserVisitor()
            visitor.visit(parsed)
            return visitor.found

        except Exception:
            return False


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
