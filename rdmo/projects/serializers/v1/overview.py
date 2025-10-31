from rest_framework import serializers

from rdmo.core.serializers import MarkdownSerializerMixin
from rdmo.projects.models import Project
from rdmo.questions.models import Catalog


class CatalogSerializer(MarkdownSerializerMixin, serializers.ModelSerializer):

    markdown_fields = ('title', )

    class Meta:
        ref_name = 'ProjectCatalogSerializer'

        model = Catalog
        fields = (
            'id',
            'title',
            'available'
        )


class ProjectOverviewSerializer(serializers.ModelSerializer):

    catalog = CatalogSerializer()

    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = (
            'id',
            'title',
            'catalog',
            'permissions',
            'created',
            'updated'
        )

    def get_permissions(self, obj):
        request = self.context.get('request')
        if request:
            return {
                'can_add_value': request.user.has_perm('projects.add_value_object', obj),
                'can_change_value': request.user.has_perm('projects.change_value_object', obj),
                'can_delete_value': request.user.has_perm('projects.delete_value_object', obj),
                'can_view_management': request.user.has_perm('management.view_management', obj)
            }
