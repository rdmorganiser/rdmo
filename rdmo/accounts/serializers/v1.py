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

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'groups',
            'role',
            'memberships',
            'is_superuser',
            'is_staff'
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
