from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
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
                'email'
            ]

    def get_full_name(self, obj) -> str:
        return get_full_name(obj)


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
            'visibility'
        )
        read_only_fields = (
            'snapshots',
        )
        validators = [
            ProjectParentValidator()
        ]

    def validate_views(self, value):
        """Block updates to views if syncing is enabled."""
        if settings.PROJECT_VIEWS_SYNC and value:
            raise serializers.ValidationError(_('Editing views is disabled.'))
        return value


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

    class Meta:
        model = Membership
        fields = (
            'id',
            'user',
            'role'
        )


class ProjectMembershipUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Membership
        fields = (
            'role',
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


class ProjectInviteSerializer(UserLookupSerializer, serializers.ModelSerializer):

    timestamp = serializers.DateTimeField(read_only=True)

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
        extra_kwargs = {
            # they must be optional because *lookup* can supply them
            "user": {"required": False, "allow_null": True},
            "email": {"required": False, "allow_null": True},
        }

    def validate_user(self, value):
        if self.context['view'].project.memberships.filter(user=value).exists():
            raise serializers.ValidationError(_('The user is already a member of the project.'))
        return value

    def validate_email(self, value):
        if self.context['view'].project.memberships.filter(user__email=value).exists():
            raise serializers.ValidationError(_('A user with that e-mail is already a member of the project.'))
        return value

    def resolve_lookup(self, value):
        User = get_user_model()
        if '@' in value:
            # ``UserLookupSerializer.validate_lookup`` already validated the format
            try:
                user = User.objects.get(email__iexact=value)
            except User.DoesNotExist:
                user = None
            except User.MultipleObjectsReturned as e:
                raise serializers.ValidationError({'lookup': _('Multiple users found with that email.')}) from e
            return user, value.lower()

        try:
            user = User.objects.get(username=value)
        except User.DoesNotExist as e:
            raise serializers.ValidationError({'lookup': _('No user with that username.')}) from e
        except User.MultipleObjectsReturned as e:
            raise serializers.ValidationError({'lookup': _('Multiple users found with that username.')}) from e
        return user, user.email



    def validate(self, data):
        User = get_user_model()

        lookup = data.pop('lookup', None)

        if lookup:
            if data.get('user') or data.get('email'):
                raise serializers.ValidationError(
                    _('`lookup` must not be combined with `user` or `email`.'),
                )
            user, email = self.resolve_lookup(lookup)
            data['user'],data['email'] = user, email

        user = data.get("user")
        email = data.get("email")

        if not user and not email:
            raise serializers.ValidationError(_('Either user, e-mail or lookup needs to be provided.'))
        elif user and email and not lookup:
            raise serializers.ValidationError(_('User and e-mail are mutually exclusive.'))

        if user:
            data['email'] = user.email
            if lookup:
                self.validate_user(user)
        if email:
            try:
                data['user'] = User.objects.get(email=email)
            except User.DoesNotExist:
                data['user'] = None
            if lookup:
                self.validate_email(email)

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


class MembershipSerializer(UserLookupSerializer, serializers.ModelSerializer):

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
