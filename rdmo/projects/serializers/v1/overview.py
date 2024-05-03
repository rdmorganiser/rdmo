from rest_framework import serializers

from rdmo.core.serializers import MarkdownSerializerMixin
from rdmo.management.rules import is_editor, is_reviewer
from rdmo.projects.models import Project
from rdmo.questions.models import Catalog


class CatalogSerializer(MarkdownSerializerMixin, serializers.ModelSerializer):

    markdown_fields = ('title', )

    class Meta:
        model = Catalog
        fields = (
            'id',
            'title',
            'available'
        )


class ProjectOverviewSerializer(serializers.ModelSerializer):

    catalog = CatalogSerializer()
    read_only = serializers.SerializerMethodField()

    is_superuser = serializers.SerializerMethodField()
    is_editor = serializers.SerializerMethodField()
    is_reviewer = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = (
            'id',
            'title',
            'catalog',
            'read_only',
            'is_superuser',
            'is_editor',
            'is_reviewer',
            'created',
            'updated'
        )

    def get_read_only(self, obj):
        request = self.context.get('request')

        if request:
            return not (request.user.has_perm('projects.add_value_object', obj) and
                        request.user.has_perm('projects.change_value_object', obj) and
                        request.user.has_perm('projects.delete_value_object', obj))
        else:
            return True

    def get_is_superuser(self, obj):
        request = self.context.get('request')
        return request.user.is_superuser

    def get_is_editor(self, obj):
        request = self.context.get('request')
        return is_editor(request.user)

    def get_is_reviewer(self, obj):
        request = self.context.get('request')
        return is_reviewer(request.user)
