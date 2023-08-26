from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site

from rest_framework import serializers

from rdmo.projects.models import Membership

from ..models import Role


class SiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Site
        fields = (
            'id',
            'name',
            'domain'
        )


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = (
            'id',
            'name'
        )


class RoleSerializer(serializers.ModelSerializer):

    member = SiteSerializer(many=True)
    manager = SiteSerializer(many=True)
    editor = SiteSerializer(many=True)
    reviewer = SiteSerializer(many=True)

    class Meta:
        model = Role
        fields = (
            'id',
            'member',
            'manager',
            'editor',
            'reviewer'
        )


class MembershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Membership
        fields = (
            'id',
            'project',
            'role'
        )


class UserSerializer(serializers.ModelSerializer):

    groups = GroupSerializer(many=True)
    role = RoleSerializer()
    memberships = MembershipSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'groups',
            'role',
            'memberships'
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
