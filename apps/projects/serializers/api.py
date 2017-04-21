from django.contrib.auth.models import User

from rest_framework import serializers

from ..models import Project, Membership, Snapshot, Value


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email'
        )


class ProjectSerializer(serializers.ModelSerializer):

    catalog = serializers.HyperlinkedRelatedField(view_name='api-v1-questions:catalog-detail', read_only=True)
    members = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = (
            'id',
            'title',
            'description',
            'catalog',
            'members'
        )

    def get_members(self, obj):
        field = UserSerializer()
        field.context = self.context

        members = {}
        for key, text in Membership.ROLE_CHOICES:
            members[key] = []
            for user in getattr(obj, key + 's'):
                members[key].append(field.to_representation(user))

        return members


class ValueSerializer(serializers.ModelSerializer):

    attribute = serializers.CharField(source='attribute.uri')
    option = serializers.CharField(source='option.uri')

    project = serializers.HyperlinkedRelatedField(view_name='api-v1-projects:project-detail', read_only=True)

    class Meta:
        model = Value
        fields = (
            'id',
            'attribute',
            'set_index',
            'collection_index',
            'text',
            'option',
            'created',
            'updated',
            'project'
        )
