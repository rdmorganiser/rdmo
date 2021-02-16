from rest_framework import serializers
from rest_framework.reverse import reverse

from rdmo.core.serializers import (MarkdownSerializerMixin, SiteSerializer,
                                   TranslationSerializerMixin)
from rdmo.core.utils import get_language_warning

from ..models import Task
from ..validators import TaskLockedValidator, TaskUniqueURIValidator


class TaskSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    key = serializers.SlugField(required=True)

    class Meta:
        model = Task
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'key',
            'comment',
            'locked',
            'available',
            'catalogs',
            'sites',
            'groups',
            'start_attribute',
            'end_attribute',
            'days_before',
            'days_after',
            'conditions'
        )
        trans_fields = (
            'title',
            'text'
        )
        validators = (
            TaskUniqueURIValidator(),
            TaskLockedValidator()
        )


class TaskIndexSerializer(MarkdownSerializerMixin, serializers.ModelSerializer):

    markdown_fields = ('text', )

    sites = SiteSerializer(many=True, read_only=True)
    warning = serializers.SerializerMethodField()
    xml_url = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            'id',
            'uri',
            'uri_prefix',
            'key',
            'locked',
            'available',
            'sites',
            'title',
            'text',
            'warning',
            'xml_url'
        )

    def get_warning(self, obj):
        return get_language_warning(obj, 'title') or get_language_warning(obj, 'text')

    def get_xml_url(self, obj):
        return reverse('v1-tasks:task-detail-export', args=[obj.pk])
