from collections.abc import Mapping
from typing import Any

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from rdmo.accounts.serializers.v1 import UserLookupSerializer
from rdmo.accounts.utils import get_full_name
from rdmo.domain.models import Attribute
from rdmo.questions.models import Catalog
from rdmo.services.validators import ProviderValidator

from ...models import (
    Integration,
    IntegrationOption,
    Invite,
    Issue,
    IssueResource,
    Membership,
    Project,
    Snapshot,
    Value,
    Visibility,
)
from ...validators import ProjectParentValidator, ValueConflictValidator, ValueQuotaValidator, ValueTypeValidator


class ProjectUserSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField()
    socialaccounts = serializers.SerializerMethodField()
    current_user = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = [
            'id',
        ]
        if settings.USER_API:
            fields += [
                'username',
                'first_name',
                'last_name',
                'full_name',
                'email',
                'socialaccounts',
                'current_user'
            ]

    def get_full_name(self, obj) -> str:
        return get_full_name(obj)

    def get_socialaccounts(self, obj) -> list[dict[str, str]]:
        if settings.SOCIALACCOUNT:
            return [{
                'provider': socialaccount.provider,
                'uid': socialaccount.uid
            } for socialaccount in obj.socialaccount_set.all()]
        else:
            return []

    def get_current_user(self, obj) -> bool:
        request = self.context.get('request')
        if request:
            return obj == request.user


class ProjectAncestorSerializer(serializers.ModelSerializer):

    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = (
            'id',
            'title',
            'permissions'
        )

    def get_permissions(self, obj) -> Mapping[str, bool]:
        request = self.context.get('request')
        view = self.context.get('view')
        if view.action == 'list':
            return {}
        else:
            return {
                'can_view_project': request.user.has_perm('projects.view_project_object', obj),
                'can_change_project': request.user.has_perm('projects.change_project_object', obj),
                'can_delete_project': request.user.has_perm('projects.delete_project_object', obj)
            }


class ProjectSerializer(serializers.ModelSerializer):

    class CatalogField(serializers.PrimaryKeyRelatedField):

        def get_queryset(self):
            return Catalog.objects.filter_for_user(self.context['request'].user)

    class ParentField(serializers.PrimaryKeyRelatedField):

        def get_queryset(self):
            return Project.objects.filter_user(self.context['request'].user)

    catalog = CatalogField(required=True)
    parent = ParentField(required=False, allow_null=True)

    owners = ProjectUserSerializer(many=True, read_only=True)
    managers = ProjectUserSerializer(many=True, read_only=True)
    authors = ProjectUserSerializer(many=True, read_only=True)
    guests = ProjectUserSerializer(many=True, read_only=True)

    permissions = serializers.SerializerMethodField()
    ancestors = serializers.SerializerMethodField()

    last_changed = serializers.DateTimeField(read_only=True)

    visibility = serializers.CharField(source='visibility.get_help_display', read_only=True)

    class Meta:
        model = Project
        fields = (
            'id',
            'title',
            'description',
            'catalog',
            'catalog_uri',
            'snapshots',
            'parent',
            'owners',
            'managers',
            'authors',
            'guests',
            'created',
            'updated',
            'last_changed',
            'site',
            'views',
            'progress_total',
            'progress_count',
            'visibility',
            'permissions',
            'ancestors'
        )
        read_only_fields = (
            'snapshots',
        )
        validators = [
            ProjectParentValidator()
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance:
            # this prefetches the ancestors of all instances for the serializer in one
            # query and caches them in the instance
            projects = self.instance if isinstance(self.instance, list) else [self.instance]
            self._prefetched_ancestors = Project.objects.prefetch_ancestors(projects)
        else:
            # prevent AttributeError for create
            self._prefetched_ancestors = {}

    def validate_views(self, value):
        """Block updates to views if syncing is enabled."""
        if settings.PROJECT_VIEWS_SYNC and value:
            raise serializers.ValidationError(_('Editing views is disabled.'))
        return value

    def get_permissions(self, obj) -> dict[str, bool]:
        request = self.context.get('request')
        view = self.context.get('view')

        if view.action == 'list':
            return {
                'can_view_project': request.user.has_perm('projects.view_project_object', obj),
                'can_change_project': request.user.has_perm('projects.change_project_object', obj),
                'can_delete_project': request.user.has_perm('projects.delete_project_object', obj)
            }
        else:
            return {
                'can_view_project': request.user.has_perm('projects.view_project_object', obj),
                'can_change_project': request.user.has_perm('projects.change_project_object', obj),
                'can_delete_project': request.user.has_perm('projects.delete_project_object', obj),
                'can_leave_project': request.user.has_perm('projects.leave_project_object', obj),
                'can_export_project': request.user.has_perm('projects.export_project_object', obj),
                'can_import_project': request.user.has_perm('projects.import_project_object', obj),
                'can_view_visibility': request.user.has_perm('projects.view_visibility_object', obj),
                'can_add_visibility': request.user.has_perm('projects.add_visibility_object', obj),
                'can_change_visibility': request.user.has_perm('projects.change_visibility_object', obj),
                'can_delete_visibility': request.user.has_perm('projects.delete_visibility_object', obj),
                'can_view_membership': request.user.has_perm('projects.view_membership_object', obj),
                'can_add_membership': request.user.has_perm('projects.add_membership_object', obj),
                'can_change_membership': request.user.has_perm('projects.change_membership_object', obj),
                'can_delete_membership': request.user.has_perm('projects.delete_membership_object', obj),
                'can_view_invite': request.user.has_perm('projects.view_invite_object', obj),
                'can_add_invite': request.user.has_perm('projects.add_invite_object', obj),
                'can_change_invite': request.user.has_perm('projects.change_invite_object', obj),
                'can_delete_invite': request.user.has_perm('projects.delete_invite_object', obj),
                'can_view_integration': request.user.has_perm('projects.view_integration_object', obj),
                'can_add_integration': request.user.has_perm('projects.add_integration_object', obj),
                'can_change_integration': request.user.has_perm('projects.change_integration_object', obj),
                'can_delete_integration': request.user.has_perm('projects.delete_integration_object', obj),
                'can_view_issue': request.user.has_perm('projects.view_issue_object', obj),
                'can_add_issue': request.user.has_perm('projects.add_issue_object', obj),
                'can_change_issue': request.user.has_perm('projects.change_issue_object', obj),
                'can_delete_issue': request.user.has_perm('projects.delete_issue_object', obj),
                'can_view_snapshot': request.user.has_perm('projects.view_snapshot_object', obj),
                'can_add_snapshot': request.user.has_perm('projects.add_snapshot_object', obj),
                'can_change_snapshot': request.user.has_perm('projects.change_snapshot_object', obj),
                'can_rollback_snapshot': request.user.has_perm('projects.rollback_snapshot_object', obj),
                'can_export_snapshot': request.user.has_perm('projects.export_snapshot_object', obj),
                'can_view_value': request.user.has_perm('projects.view_value_object', obj),
                'can_add_value': request.user.has_perm('projects.add_value_object', obj),
                'can_change_value': request.user.has_perm('projects.change_value_object', obj),
                'can_delete_value': request.user.has_perm('projects.delete_value_object', obj)
            }

    def get_ancestors(self, obj) -> list[dict[str, Any]]:
        ancestors = self._prefetched_ancestors.get(obj.id, obj.get_ancestors())
        return ProjectAncestorSerializer(ancestors, many=True, context=self.context).data


class ProjectCopySerializer(ProjectSerializer):

    class Meta:
        model = Project
        fields = ProjectSerializer.Meta.fields
        read_only_fields = ProjectSerializer.Meta.read_only_fields


class ProjectVisibilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Visibility
        fields = (
            'project',
            'sites',
            'groups'
        )


class ProjectMembershipSerializer(serializers.ModelSerializer):

    user = ProjectUserSerializer(read_only=True)

    class Meta:
        model = Membership
        fields = (
            'id',
            'user',
            'role'
        )


class ProjectMembershipCreateSerializer(UserLookupSerializer, serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(), allow_null=True, required=False
    )
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Membership
        fields = (
            'id',
            'user',
            'role',
            'lookup',  # write-only
            'first_name',  # read-only
            'last_name',  # read-only
            'email',  # read-only
        )

    def validate_user(self, value):
        if self.context["view"].project.memberships.filter(user=value).exists():
            raise serializers.ValidationError(_("The user is already a member of the project."))
        return value

    def validate(self, data):
        lookup = data.pop("lookup", None)
        if lookup:
            if data.get("user"):
                raise serializers.ValidationError(_("Cannot combine `lookup` and `user`."))
            user, _email = self.resolve_lookup(lookup)
            self.validate_user(user)
            data["user"] = user

        user = data.get("user")
        if not user:
            raise serializers.ValidationError(_("User must be provided via `user` or `lookup`."))

        return data


class ProjectMembershipUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Membership
        fields = (
            'role',
        )


class ProjectMembershipHierarchySerializer(serializers.ModelSerializer):

    user = ProjectUserSerializer(read_only=True)
    project = ProjectAncestorSerializer(read_only=True)

    class Meta:
        model = Membership
        fields = (
            'id',
            'user',
            'role',
            'project'
        )


class ProjectIntegrationOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = IntegrationOption
        fields = (
            'key',
            'value'
        )


class ProjectIntegrationSerializer(serializers.ModelSerializer):

    options = ProjectIntegrationOptionSerializer(many=True)

    class Meta:
        model = Integration
        fields = (
            'id',
            'provider_key',
            'options'
        )
        validators = [
            ProviderValidator()
        ]

    def create(self, validated_data):
        provider_key = validated_data.get('provider_key')
        project = validated_data.get('project')
        options = {option.get('key'): option.get('value') for option in validated_data.get('options', [])}

        integration = Integration(project=project, provider_key=provider_key)
        integration.save()
        integration.save_options(options)

        return integration

    def update(self, integration, validated_data):
        options = {option.get('key'): option.get('value') for option in validated_data.get('options', [])}

        integration.save_options(options)

        return integration


class ProjectInviteSerializer(serializers.ModelSerializer):

    user = ProjectUserSerializer(read_only=True)

    class Meta:
        model = Invite
        fields = (
            'id',
            'user',
            'email',
            'role',
            'timestamp'
        )


class ProjectInviteCreateSerializer(UserLookupSerializer, serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(), allow_null=True, required=False
    )
    email = serializers.EmailField(required=False, allow_null=True)

    class Meta:
        model = Invite
        fields = (
            'id',
            'user',
            'email',
            'role',
            'lookup',
            'timestamp'
        )

    def validate_user(self, value):
        if self.context['view'].project.memberships.filter(user=value).exists():
            raise serializers.ValidationError(_('The user is already a member of the project.'))
        return value

    def validate_email(self, value):
        if self.context['view'].project.memberships.filter(user__email=value).exists():
            raise serializers.ValidationError(_('A user with that e-mail is already a member of the project.'))
        return value

    def validate(self, data):
        User = get_user_model()

        lookup = data.pop('lookup', None)

        if lookup:
            if data.get('user') or data.get('email'):
                raise serializers.ValidationError(
                    _('lookup must not be combined with user or email.'),
                )
            user, email = self.resolve_lookup(lookup)
            if user:
                self.validate_user(user)
            if email:
                self.validate_email(email)
            data["user"], data["email"] = user, email

        user = data.get("user")
        email = data.get("email")

        if not user and not email and not lookup:
            raise serializers.ValidationError(_('Either user, e-mail or lookup needs to be provided.'))
        elif user and email and not lookup:
            raise serializers.ValidationError(_('User and e-mail are mutually exclusive.'))

        if user:
            data['email'] = user.email

        if email:
            try:
                data['user'] = User.objects.get(email=email)
            except User.DoesNotExist:
                data['user'] = None

        return data

    def create(self, validated_data):
        invite = super().create(validated_data)
        invite.make_token()
        invite.save()
        return invite


class ProjectInviteUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invite
        fields = (
            'role',
        )


class ProjectIssueResourceSerializer(serializers.ModelSerializer):

    integration = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = IssueResource
        fields = (
            'id',
            'integration',
            'url'
        )


class ProjectIssueSerializer(serializers.ModelSerializer):

    task = serializers.PrimaryKeyRelatedField(read_only=True)
    resources = ProjectIssueResourceSerializer(read_only=True, many=True)

    class Meta:
        model = Issue
        fields = (
            'id',
            'task',
            'status',
            'resources'
        )


class ProjectSnapshotSerializer(serializers.ModelSerializer):

    class Meta:
        model = Snapshot
        fields = (
            'id',
            'title',
            'description'
        )


class ProjectValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Value
        fields = (
            'id',
            'created',
            'updated',
            'attribute',
            'attribute_uri',
            'set_prefix',
            'set_index',
            'set_collection',
            'collection_index',
            'text',
            'option',
            'option_uri',
            'file_name',
            'file_url',
            'value_type',
            'unit',
            'external_id'
        )
        validators = (
            ValueConflictValidator(),
            ValueQuotaValidator(),
            ValueTypeValidator()
        )


class MembershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Membership
        fields = (
            'id',
            'project',
            'user',
            'role'
        )



class IntegrationSerializer(serializers.ModelSerializer):

    options = ProjectIntegrationOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Integration
        fields = (
            'id',
            'project',
            'provider_key',
            'options'
        )


class InviteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invite
        fields = (
            'id',
            'project',
            'user',
            'email',
            'role',
            'timestamp'
        )

class UserInviteSerializer(InviteSerializer):

    title = serializers.CharField(source='project.title', read_only=True)
    description = serializers.CharField(source='project.description', read_only=True)

    class Meta:
        model = Invite
        fields = (
            *InviteSerializer.Meta.fields,
            'title',
            'description',
            'token',
        )

class IssueResourceSerializer(serializers.ModelSerializer):

    integration = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = IssueResource
        fields = (
            'id',
            'integration',
            'url'
        )


class IssueSerializer(serializers.ModelSerializer):

    project = serializers.PrimaryKeyRelatedField(read_only=True)
    task = serializers.PrimaryKeyRelatedField(read_only=True)
    resources = IssueResourceSerializer(read_only=True, many=True)

    class Meta:
        model = Issue
        fields = (
            'id',
            'project',
            'task',
            'status',
            'resources'
        )


class SnapshotSerializer(serializers.ModelSerializer):

    class Meta:
        model = Snapshot
        fields = (
            'id',
            'project',
            'title',
            'description',
            'created',
            'updated'
        )


class ValueSerializer(serializers.ModelSerializer):

    attribute = serializers.PrimaryKeyRelatedField(queryset=Attribute.objects.all(), required=True)

    class Meta:
        model = Value
        fields = (
            'id',
            'created',
            'updated',
            'project',
            'snapshot',
            'attribute',
            'attribute_uri',
            'set_prefix',
            'set_index',
            'set_collection',
            'collection_index',
            'text',
            'option',
            'option_uri',
            'file_name',
            'file_url',
            'value_type',
            'unit',
            'external_id'
        )


class ValueSearchSerializer(serializers.ModelSerializer):

    project_label = serializers.CharField(source='project.title', required=False, read_only=True)
    snapshot_label = serializers.CharField(source='snapshot.title', required=False, read_only=True)
    set_label = serializers.CharField(required=False, read_only=True)
    value_label = serializers.CharField(source='label', read_only=True)

    class Meta:
        model = Value
        fields = (
            'id',
            'attribute',
            'project_label',
            'snapshot_label',
            'set_label',
            'value_label',
            'set_prefix',
            'set_index',
            'set_collection',
            'collection_index',
            'text',
            'option',
            'external_id'
        )
