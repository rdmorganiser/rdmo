from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from rdmo.questions.models import Catalog
from rdmo.services.validators import ProviderValidator

from ...models import Integration, IntegrationOption, Invite, Issue, IssueResource, Membership, Project, Snapshot, Value
from ...validators import ValueValidator


class UserSerializer(serializers.ModelSerializer):

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
                'email'
            ]


class ProjectSerializer(serializers.ModelSerializer):

    class CatalogField(serializers.PrimaryKeyRelatedField):

        def get_queryset(self):
            return Catalog.objects.filter_current_site() \
                                  .filter_group(self.context['request'].user) \
                                  .filter_availability(self.context['request'].user) \
                                  .order_by('-available', 'order')

    class ParentField(serializers.PrimaryKeyRelatedField):

        def get_queryset(self):
            return Project.objects.filter_user(self.context['request'].user)

    catalog = CatalogField(required=True)
    parent = ParentField(required=False)

    owners = UserSerializer(many=True, read_only=True)
    managers = UserSerializer(many=True, read_only=True)
    authors = UserSerializer(many=True, read_only=True)
    guests = UserSerializer(many=True, read_only=True)

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
            'site',
            'views'
        )
        read_only_fields = (
            'snapshots',
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


class ProjectInviteSerializer(serializers.ModelSerializer):

    timestamp = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Invite
        fields = (
            'id',
            'user',
            'email',
            'role',
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
        user = data.get('user')
        email = data.get('email')

        if not user and not email:
            raise serializers.ValidationError(_('Either user or e-mail needs to be provided.'))
        elif user and email:
            raise serializers.ValidationError(_('User and e-mail are mutually exclusive.'))
        elif user:
            data['email'] = user.email
        elif email:
            usermodel = get_user_model()
            try:
                data['user'] = usermodel.objects.get(email=email)
            except usermodel.DoesNotExist:
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
        validators = (ValueValidator(), )


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
