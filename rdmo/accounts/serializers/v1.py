from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from rdmo.projects.models import Invite, Membership

from ..models import Role


class UserSiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Site
        fields = (
            'id',
            'name',
            'domain'
        )


class UserGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = (
            'id',
            'name'
        )


class UserRoleSerializer(serializers.ModelSerializer):

    member = UserSiteSerializer(many=True)
    manager = UserSiteSerializer(many=True)
    editor = UserSiteSerializer(many=True)
    reviewer = UserSiteSerializer(many=True)

    class Meta:
        model = Role
        fields = (
            'id',
            'member',
            'manager',
            'editor',
            'reviewer'
        )


class UserMembershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Membership
        fields = (
            'id',
            'project',
            'role'
        )


class UserSerializer(serializers.ModelSerializer):

    groups = UserGroupSerializer(many=True)
    role = UserRoleSerializer()
    memberships = UserMembershipSerializer(many=True)

    is_site_manager = serializers.BooleanField(source='role.is_site_manager')

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'groups',
            'role',
            'memberships',
            'is_superuser',
            'is_staff',
            'is_site_manager'
        ]
        if settings.USER_API:
            fields += [
                'username',
                'first_name',
                'last_name',
                'email',
                'last_login',
                'date_joined',
            ]


class CurrentUserSerializer(UserSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = [
            *UserSerializer.Meta.fields,
            'permissions',
        ]

    def get_permissions(self, obj) -> dict[str, bool]:
        return {
            'can_view_project': obj.has_perm('projects.view_project'),
            'can_change_project': obj.has_perm('projects.change_project'),
            'can_delete_project': obj.has_perm('projects.delete_project'),
            'can_leave_project': obj.has_perm('projects.leave_project'),
            'can_export_project': obj.has_perm('projects.export_project'),
            'can_import_project': obj.has_perm('projects.import_project'),
            'can_view_visibility': obj.has_perm('projects.view_visibility'),
            'can_add_visibility': obj.has_perm('projects.add_visibility'),
            'can_change_visibility': obj.has_perm('projects.change_visibility'),
            'can_delete_visibility': obj.has_perm('projects.delete_visibility'),
            'can_view_membership': obj.has_perm('projects.view_membership'),
            'can_add_membership': obj.has_perm('projects.add_membership'),
            'can_change_membership': obj.has_perm('projects.change_membership'),
            'can_delete_membership': obj.has_perm('projects.delete_membership'),
            'can_view_invite': obj.has_perm('projects.view_invite'),
            'can_add_invite': obj.has_perm('projects.add_invite'),
            'can_change_invite': obj.has_perm('projects.change_invite'),
            'can_delete_invite': obj.has_perm('projects.delete_invite'),
            'can_view_integration': obj.has_perm('projects.view_integration'),
            'can_add_integration': obj.has_perm('projects.add_integration'),
            'can_change_integration': obj.has_perm('projects.change_integration'),
            'can_delete_integration': obj.has_perm('projects.delete_integration'),
            'can_view_issue': obj.has_perm('projects.view_issue'),
            'can_add_issue': obj.has_perm('projects.add_issue'),
            'can_change_issue': obj.has_perm('projects.change_issue'),
            'can_delete_issue': obj.has_perm('projects.delete_issue'),
            'can_view_snapshot': obj.has_perm('projects.view_snapshot'),
            'can_add_snapshot': obj.has_perm('projects.add_snapshot'),
            'can_change_snapshot': obj.has_perm('projects.change_snapshot'),
            'can_delete_snapshot': obj.has_perm('projects.delete_snapshot'),
            'can_rollback_snapshot': obj.has_perm('projects.rollback_snapshot'),
            'can_export_snapshot': obj.has_perm('projects.export_snapshot'),
            'can_view_value': obj.has_perm('projects.view_value'),
            'can_add_value': obj.has_perm('projects.add_value'),
            'can_change_value': obj.has_perm('projects.change_value'),
            'can_delete_value': obj.has_perm('projects.delete_value')
        }


class UserLookupSerializer(serializers.Serializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    lookup = serializers.CharField(
        required=False, write_only=True, help_text=_("The username or e-mail of the user.")
    )

    def validate_lookup(self, value: str) -> str:
        if "@" in value:
            validator = EmailValidator()
            try:
                validator(value)
            except ValidationError as e:
                raise serializers.ValidationError(validator.message) from e
        return value

    def resolve_lookup(self, value):
        User = get_user_model()

        # 1) Try exact username match first — even if it contains '@'
        try:
            user = User.objects.get(username=value)
        except User.DoesNotExist:
            # 2) Try case-insensitive email match
            try:
                user = User.objects.get(email__iexact=value)
            except User.DoesNotExist as e:
                if (
                    "@" in value and
                    self.Meta.model is Invite and
                    settings.PROJECT_SEND_INVITE
                ):
                    # return an email when invite send is allowed
                    return None, value
                raise serializers.ValidationError({"lookup": _("No user found.")}) from e
            except User.MultipleObjectsReturned as e:
                raise serializers.ValidationError({"lookup": _("Multiple users found with that e-mail.")}) from e
            else:
                return user, user.email
        except User.MultipleObjectsReturned as e:
            raise serializers.ValidationError({'lookup': _('Multiple users found with that username.')}) from e
        else:
            return user, user.email
