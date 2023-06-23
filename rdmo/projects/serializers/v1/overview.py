from rest_framework import serializers

from rdmo.projects.models import Project
from rdmo.questions.models import Catalog, Page, Section


class PageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = (
            'id',
            'title',
            'has_conditions'
        )


class SectionSerializer(serializers.ModelSerializer):

    pages = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = (
            'id',
            'title',
            'pages'
        )

    def get_pages(self, obj):
        return PageSerializer(obj.elements, many=True, read_only=True).data


class CatalogSerializer(serializers.ModelSerializer):

    sections = serializers.SerializerMethodField()

    class Meta:
        model = Catalog
        fields = (
            'id',
            'title',
            'sections'
        )

    def get_sections(self, obj):
        return SectionSerializer(obj.elements, many=True, read_only=True).data


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
