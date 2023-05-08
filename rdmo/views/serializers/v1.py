from django.template import Context, Template, TemplateSyntaxError
from rest_framework import exceptions, serializers

from rdmo.core.serializers import (ElementExportSerializerMixin,
                                   ElementWarningSerializerMixin,
                                   TranslationSerializerMixin)

from ..models import View
from ..validators import ViewLockedValidator, ViewUniqueURIValidator


class ViewSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    key = serializers.SlugField(required=True)

    def validate(self, data):
        # try to render the template to see that the syntax is ok (if the editor was used)
        if self.context['request'].data.get('editor'):
            try:
                Template(data['template']).render(Context({}))
            except (KeyError, IndexError):
                pass
            except (TemplateSyntaxError, TypeError) as e:
                raise exceptions.ValidationError({'template': '\n'.join(e.args)})

        return super(ViewSerializer, self).validate(data)

    class Meta:
        model = View
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
            'template',
            'title',
            'help'
        )
        trans_fields = (
            'title',
            'help'
        )
        validators = (
            ViewUniqueURIValidator(),
            ViewLockedValidator()
        )


class ViewListSerializer(ElementExportSerializerMixin, ElementWarningSerializerMixin,
                         ViewSerializer):

    warning = serializers.SerializerMethodField()
    xml_url = serializers.SerializerMethodField()

    class Meta(ViewSerializer.Meta):
        fields = ViewSerializer.Meta.fields + (
            'warning',
            'xml_url'
        )
        warning_fields = (
            'title',
        )


class ViewIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = View
        fields = (
            'id',
            'uri'
        )
