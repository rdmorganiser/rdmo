from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from rest_framework import serializers
from rest_framework.utils import model_meta

from rdmo.core.utils import get_languages, markdown2html


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


class ThroughModelSerializerMixin(object):

    def create(self, validated_data):
        through_fields = self.get_through_fields(validated_data)
        instance = super().create(validated_data)
        instance = self.set_through_fields(instance, through_fields)
        return instance

    def update(self, instance, validated_data):
        through_fields = self.get_through_fields(validated_data)
        instance = super().update(instance, validated_data)
        instance = self.set_through_fields(instance, through_fields)
        return instance

    def get_through_fields(self, validated_data):
        model_info = model_meta.get_field_info(self.Meta.model)

        through_fields = {}
        for field_name in self.Meta.through_fields:
            # get the through model, e.g. CatalogSection
            through_model = model_info.reverse_relations[field_name].related_model

            # loop over the fields of the through model
            through_info = model_meta.get_field_info(through_model)
            for field in through_info.forward_relations:
                if field_name.endswith(f'_{field}s'):
                    forward_field = field
                else:
                    instance_field = field

            through_fields[field_name] = {
                'model': through_model,
                'fields': {
                    'instance': instance_field,
                    'forward': forward_field,
                },
                'validated_data': validated_data.pop(field_name, None)
            }

        return through_fields

    def set_through_fields(self, instance, through_fields):
        for field_name, field_config in through_fields.items():
            if field_config['validated_data'] is not None:
                old_list = list(getattr(instance, field_name).all())
                new_list = []

                for field_data in field_config['validated_data']:
                    try:
                        # look for the item in old_list
                        old_item = next(filter(lambda old_item: getattr(old_item, field_config['fields']['forward']) ==
                                               field_data.get(field_config['fields']['forward']), old_list))
                        # update oder if it changed
                        if old_item.order != field_data.get('order'):
                            old_item.order == field_data.get('order')
                            old_item.save()

                        # remove it from the old list so that it won't get removed
                        old_list.remove(old_item)
                    except StopIteration:
                        # create a new item
                        new_data = dict({
                            field_config['fields']['instance']: instance
                        }, **field_data)
                        new_item = field_config['model'](**new_data)
                        new_item.save()
                        new_list.append(new_item)

                # remove the remainders of the old list
                for old_item in old_list:
                    old_item.delete()

        return instance


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
