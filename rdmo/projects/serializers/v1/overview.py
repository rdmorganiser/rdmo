from rest_framework import serializers

from rdmo.projects.models import Project
from rdmo.questions.models import Catalog


class CatalogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Catalog
        fields = (
            'id',
            'title'
        )


class ProjectOverviewSerializer(serializers.ModelSerializer):

    catalog = CatalogSerializer()
    read_only = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = (
            'id',
            'title',
            'catalog',
            'read_only',
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
