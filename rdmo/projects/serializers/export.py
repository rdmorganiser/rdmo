import base64

from rest_framework import serializers

from ..models import Membership, Project, Snapshot, Value
from .v1 import ProjectUserSerializer


class ValueSerializer(serializers.ModelSerializer):

    attribute = serializers.CharField(source='attribute.uri', default=None, read_only=True)
    option = serializers.CharField(source='option.uri', default=None, read_only=True)
    file_content = serializers.SerializerMethodField()

    class Meta:
        model = Value
        fields = (
            'attribute',
            'set_prefix',
            'set_index',
            'set_collection',
            'collection_index',
            'text',
            'option',
            'file_name',
            'file_content',
            'value_type',
            'unit',
            'external_id',
            'created',
            'updated'
        )

    def get_file_content(self, obj):
        if not obj.file:
            return None

        try:
            return base64.b64encode(obj.file.read())
        except FileNotFoundError:
            # file was saved but no longer exists
            return None


class SnapshotSerializer(serializers.ModelSerializer):

    values = serializers.SerializerMethodField()

    catalog = serializers.CharField(source='catalog.uri', default=None, read_only=True)
    tasks = serializers.SerializerMethodField()
    views = serializers.SerializerMethodField()
    memberships = serializers.SerializerMethodField()  # optional, from context

    class Meta:
        model = Snapshot
        fields = (
            'title',
            'description',
            'catalog',
            'tasks',
            'views',
            'values',
            'memberships',  # optional, from context
            'created',
            'updated'
        )

    def get_values(self, obj):
        values = Value.objects.filter(project=obj.project, snapshot=obj) \
                              .select_related('attribute', 'option')
        serializer = ValueSerializer(instance=values, many=True)
        return serializer.data

    def get_tasks(self, obj):
        return [task.uri for task in obj.project.tasks.all()]

    def get_views(self, obj):
        return [view.uri for view in obj.project.views.all()]

    def get_memberships(self, obj):
        if not self.context.get("include_memberships"):
            return []
        qs = obj.project.memberships.select_related("user").all()
        return MembershipForExportSerializer(qs, many=True, context=self.context).data


class ProjectSnapshotSerializer(serializers.ModelSerializer):

    values = serializers.SerializerMethodField()

    class Meta:
        model = Snapshot
        fields = (
            'title',
            'description',
            'values',
            'created',
            'updated'
        )

    def get_values(self, obj):
        values = Value.objects.filter(snapshot=obj).select_related('attribute', 'option')
        serializer = ValueSerializer(instance=values, many=True)
        return serializer.data


class ProjectSerializer(serializers.ModelSerializer):

    snapshots = ProjectSnapshotSerializer(many=True)
    values = serializers.SerializerMethodField()
    memberships = serializers.SerializerMethodField()  # optional from context

    catalog = serializers.CharField(source='catalog.uri', default=None, read_only=True)
    tasks = serializers.SerializerMethodField()
    views = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = (
            'title',
            'description',
            'catalog',
            'tasks',
            'views',
            'snapshots',
            'values',
            'memberships',  # optional, from context
            'created',
            'updated'
        )

    def get_values(self, obj):
        values = Value.objects.filter(project=obj, snapshot=None).select_related('attribute', 'option')
        serializer = ValueSerializer(instance=values, many=True)
        return serializer.data

    def get_tasks(self, obj):
        return [task.uri for task in obj.tasks.all()]

    def get_views(self, obj):
        return [view.uri for view in obj.views.all()]

    def get_memberships(self, obj):
        if not self.context.get("include_memberships"):
            return []
        qs = obj.memberships.select_related("user").all()
        return MembershipForExportSerializer(qs, many=True, context=self.context).data


class MembershipForExportSerializer(serializers.ModelSerializer):
    user = ProjectUserSerializer(read_only=True)

    class Meta:
        model = Membership
        fields = ("user", "role")
