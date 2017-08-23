from django.contrib.auth.models import User

from rest_framework import serializers

from ..models import Project, Membership, Snapshot, Value


class ProjectSerializer(serializers.ModelSerializer):

    catalog = serializers.HyperlinkedRelatedField(view_name='api-v1-questions:catalog-detail', read_only=True)
    snapshots = serializers.HyperlinkedRelatedField(view_name='api-v1-projects:snapshot-detail', read_only=True, many=True)
    members = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = (
            'id',
            'title',
            'description',
            'catalog',
            'snapshots',
            'members'
        )

    def get_members(self, obj):
        field = serializers.HyperlinkedRelatedField(view_name='api-v1-accounts:user-detail', read_only=True)
        field.context = self.context

        members = {}
        for key, text in Membership.ROLE_CHOICES:
            members[key] = []
            for user in getattr(obj, key + 's'):
                members[key].append(field.to_representation(user))

        return members


class SnapshotSerializer(serializers.ModelSerializer):

    project = serializers.HyperlinkedRelatedField(view_name='api-v1-projects:project-detail', read_only=True)

    class Meta:
        model = Snapshot
        fields = (
            'id',
            'project',
            'title',
            'description'
        )


class ValueSerializer(serializers.ModelSerializer):

    project = serializers.HyperlinkedRelatedField(view_name='api-v1-projects:project-detail', read_only=True)

    attribute = serializers.HyperlinkedRelatedField(view_name='api-v1-domain:attribute-detail', read_only=True)
    option = serializers.HyperlinkedRelatedField(view_name='api-v1-options:option-detail', read_only=True)

    class Meta:
        model = Value
        fields = (
            'id',
            'project',
            'attribute',
            'set_index',
            'collection_index',
            'text',
            'option',
            'created',
            'updated'
        )
