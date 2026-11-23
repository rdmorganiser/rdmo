from django.db.models.manager import BaseManager

from rest_framework import serializers

from rdmo.domain.models import Attribute
from rdmo.options.models import Option
from rdmo.questions.models import Catalog

from ..models import Project, Snapshot, Value


class ImportListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        # the import plugins create unsaved instances, which cannot use their related managers,
        # instead the related objects are stored in private attributes, e.g. project._values,
        # which are used here as a fallback for the manager
        if isinstance(data, BaseManager) and data.instance.pk is None:
            data = getattr(data.instance, f'_{self.field_name}', [])
        return super().to_representation(data)


class ProjectCatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = (
            'id',
            'uri',
            'title',
            'help',
        )


class ProjectAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = (
            'id',
            'uri',
        )


class ProjectOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = (
            'id',
            'uri',
        )


class ProjectValueSerializer(serializers.ModelSerializer):
    file_name = serializers.CharField(source='_file_name')
    attribute = ProjectAttributeSerializer()
    option = ProjectOptionSerializer()

    class Meta:
        model = Value
        list_serializer_class = ImportListSerializer
        fields = (
            'attribute',
            'set_prefix',
            'set_index',
            'set_collection',
            'collection_index',
            'text',
            'option',
            'external_id',
            'file_name',
            'value_type',
            'unit',
            'created',
            'updated',
        )


class ProjectSnapshotSerializer(serializers.ModelSerializer):
    values = ProjectValueSerializer(many=True)

    class Meta:
        model = Snapshot
        list_serializer_class = ImportListSerializer
        fields = (
            'title',
            'description',
            'created',
            'updated',
            'values',
        )


class ProjectSerializer(serializers.ModelSerializer):
    catalog = ProjectCatalogSerializer()
    snapshots = ProjectSnapshotSerializer(many=True)
    values = ProjectValueSerializer(many=True)

    class Meta:
        model = Project
        fields = (
            'title',
            'description',
            'created',
            'updated',
            'catalog',
            'snapshots',
            'values',
        )
