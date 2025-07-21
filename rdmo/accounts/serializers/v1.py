from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site

from rest_framework import serializers

from rdmo.projects.models import Membership

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
