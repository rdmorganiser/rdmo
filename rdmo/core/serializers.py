import logging

from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from rest_framework import serializers

from rdmo.core.utils import get_languages, markdown2html

logger = logging.getLogger(__name__)

class RecursiveField(serializers.Serializer):

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ChoicesSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj[0]

    def get_text(self, obj):
        return obj[1]


class MarkdownSerializerMixin(serializers.Serializer):

    markdown_fields = ()

    def to_representation(self, instance):
        response = super(MarkdownSerializerMixin, self).to_representation(instance)

        for markdown_field in self.markdown_fields:
            if markdown_field in response and response[markdown_field]:
                response[markdown_field] = markdown2html(response[markdown_field])

        return response


class TranslationSerializerMixin(object):

    def __init__(self, *args, **kwargs):
        super(TranslationSerializerMixin, self).__init__(*args, **kwargs)

        meta = getattr(self, 'Meta', None)
        if meta:
            for lang_code, lang_string, lang_field in get_languages():
                for field in meta.trans_fields:
                    field_name = '%s_%s' % (field, lang_field)
                    model_field = meta.model._meta.get_field(field_name)

                    self.fields['%s_%s' % (field, lang_code)] = serializers.CharField(
                        source=field_name,
                        required=not model_field.blank,
                        allow_null=model_field.null,
                        allow_blank=model_field.blank)


class ReadOnlyObjectPermissionsSerializerMixin(object):
    '''
    A mixin class for Serializers that adds a boolean field with the name read_only.
    It checks the object permissions based on the model of the serializer.
    
    Requires:
        - the request object in the context kwargs of the Serializer call:
            ..., context={'request': request}
        - so that this mixin has self.context['request']

    In the Serializer class add:
        read_only = serializers.SerializerMethodField(read_only=True)
    and the field to fields:
        read_only
    '''
    
    OBJECT_PERMISSION_ACTION_NAMES = ('change', 'delete')
    
    @staticmethod
    def construct_object_permission(model, action_name: str) -> str:
        model_app_label = model._meta.app_label
        model_name = model._meta.model_name
        perm = f'{model_app_label}.{action_name}_{model_name}_object'
        return perm

    def get_read_only(self, obj) -> bool:
        user = self.context['request'].user
        perms = (self.construct_object_permission(self.Meta.model, action_name)
                    for action_name in self.OBJECT_PERMISSION_ACTION_NAMES)
        return not all(user.has_perm(perm, obj) for perm in perms)


class SiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Site
        fields = (
            'id',
            'domain',
            'name'
        )


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = (
            'id',
            'name'
        )
