import logging

from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.db.models import Max

from rest_framework import serializers
from rest_framework.utils import model_meta

from rdmo.core.utils import get_language_warning, get_languages, markdown2html

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
        response = super().to_representation(instance)

        for markdown_field in self.markdown_fields:
            if markdown_field in response and response[markdown_field]:
                response[markdown_field] = markdown2html(response[markdown_field])

        return response


class TranslationSerializerMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        meta = getattr(self, 'Meta', None)
        if meta is None:
            return

        for lang_code, lang_string, lang_field in get_languages():
            for field in meta.trans_fields:
                field_name = f'{field}_{lang_field}'
                model_field = meta.model._meta.get_field(field_name)

                self.fields[f'{field}_{lang_code}'] = serializers.CharField(
                    source=field_name,
                    required=not model_field.blank,
                    allow_null=model_field.null,
                    allow_blank=model_field.blank)


class ThroughModelSerializerMixin:

    def create(self, validated_data):
        parent_fields = self.get_parent_fields(validated_data)
        through_fields = self.get_through_fields(validated_data)
        instance = super().create(validated_data)
        instance = self.set_through_fields(instance, through_fields)
        instance = self.set_parent_fields(instance, parent_fields)
        return instance

    def update(self, instance, validated_data):
        self.get_parent_fields(validated_data)
        through_fields = self.get_through_fields(validated_data)
        instance = super().update(instance, validated_data)
        instance = self.set_through_fields(instance, through_fields)
        return instance

    def get_through_fields(self, validated_data):
        try:
            self.Meta.through_fields
        except AttributeError:
            return None

        model_info = model_meta.get_field_info(self.Meta.model)

        through_fields = {}
        for field_name, source_name, target_name, through_name in self.Meta.through_fields:
            through_model = model_info.reverse_relations[through_name].related_model
            through_fields[field_name] = (through_model, validated_data.pop(through_name, None))

        return through_fields

    def set_through_fields(self, instance, through_fields):
        try:
            self.Meta.through_fields
        except AttributeError:
            return instance

        for field_name, source_name, target_name, through_name in self.Meta.through_fields:
            through_model, validated_data = through_fields[field_name]
            if validated_data is None:
                continue

            items = list(getattr(instance, through_name).all())

            for data in validated_data:
                try:
                    # look for the item in items
                    item = next(filter(lambda item: getattr(item, target_name) == data.get(target_name), items))
                    # update order if the item if it changed
                    if item.order != data.get('order'):
                        item.order = data.get('order')
                        item.save()

                    # remove the item from the items list so that it won't get removed
                    items.remove(item)
                except StopIteration:
                    # create a new item
                    new_data = dict({
                        source_name: instance
                    }, **data)
                    new_item = through_model(**new_data)
                    new_item.save()

            # remove the remainders of the items list
            for item in items:
                item.delete()

        return instance

    def get_parent_fields(self, validated_data):
        try:
            self.Meta.parent_fields
        except AttributeError:
            return None

        model_info = model_meta.get_field_info(self.Meta.model)

        parent_fields = {}
        for field_name, source_name, target_name, through_name in self.Meta.parent_fields:
            parent_model = model_info.reverse_relations[field_name].related_model
            parent_model_info = model_meta.get_field_info(parent_model)

            through_model = parent_model_info.reverse_relations[through_name].related_model

            parent_fields[field_name] = (through_model, validated_data.pop(field_name, None))

        return parent_fields

    def set_parent_fields(self, instance, parent_fields):
        try:
            self.Meta.parent_fields
        except AttributeError:
            return instance

        for field_name, source_name, target_name, through_name in self.Meta.parent_fields:
            through_model, validated_data = parent_fields[field_name]

            if validated_data is None:
                continue

            for parent in validated_data:
                order = (getattr(parent, through_name).aggregate(order=Max('order')).get('order') or 0) + 1
                through_model(**{
                    source_name: parent,
                    target_name: instance,
                    'order': order
                }).save()

        return instance


class ElementModelSerializerMixin(serializers.ModelSerializer):

    def get_model(self, obj):
        # return the model name in the form "domain.attribute"
        return str(self.Meta.model._meta)


class ElementWarningSerializerMixin(serializers.ModelSerializer):

    def get_warning(self, obj):
        return any(get_language_warning(obj, field_name) for field_name in self.Meta.warning_fields)


class ReadOnlyObjectPermissionSerializerMixin:
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

    current = serializers.SerializerMethodField()

    class Meta:
        model = Site
        fields = (
            'id',
            'domain',
            'name',
            'current'
        )

    def get_current(self, obj):
        return obj == Site.objects.get_current()


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = (
            'id',
            'name'
        )
