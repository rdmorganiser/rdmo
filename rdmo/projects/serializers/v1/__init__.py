from rest_framework import serializers

from rdmo.accounts.serializers.v1 import UserSerializer

from ...models import Project, Membership, Snapshot, Value


class ProjectSerializer(serializers.ModelSerializer):

    read_only = serializers.SerializerMethodField()
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
            'snapshots',
            'read_only',
            'owners',
            'managers',
            'authors',
            'guests'
        )
        read_only_fields = (
            'snapshots',
        )

    def get_read_only(self, obj):
        request = self.context.get('request')

        if request:
            return not (request.user.has_perm('projects.add_value_object', obj) and
                        request.user.has_perm('projects.change_value_object', obj) and
                        request.user.has_perm('projects.delete_value_object', obj))
        else:
            return True


class ProjectMembershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Membership
        fields = (
            'id',
            'user',
            'role'
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
            'set_index',
            'collection_index',
            'text',
            'option',
            'value_type',
            'unit'
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


class SnapshotSerializer(serializers.ModelSerializer):

    class Meta:
        model = Snapshot
        fields = (
            'id',
            'project',
            'title',
            'description'
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
            'set_index',
            'collection_index',
            'text',
            'option',
            'value_type',
            'unit'
        )
