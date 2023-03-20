from django.template import Context, Template, TemplateSyntaxError
from rest_framework import exceptions, serializers

from rdmo.core.serializers import (ElementExportSerializerMixin,
                                   ElementModelSerializerMixin,
                                   ElementWarningSerializerMixin,
                                   TranslationSerializerMixin,
                                   CanEditObjectSerializerMixin)

from ..models import View
from ..validators import ViewLockedValidator, ViewUniqueURIValidator


class BaseViewSerializer(CanEditObjectSerializerMixin, TranslationSerializerMixin, 
                        ElementModelSerializerMixin, serializers.ModelSerializer):

    model = serializers.SerializerMethodField()
    can_edit = serializers.SerializerMethodField()


    class Meta:
        model = View
        fields = (
            'id',
            'model',
            'uri',
            'uri_prefix',
            'key',
            'comment',
            'locked',
            'available',
            'catalogs',
            'sites',
            'can_edit',
            'groups',
            'template',
            'title',
            'help'
        )
        trans_fields = (
            'title',
            'help'
        )


class ViewSerializer(BaseViewSerializer):

    key = serializers.SlugField(required=True)
    projects_count = serializers.IntegerField(read_only=True)

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

    class Meta(BaseViewSerializer.Meta):
        fields = BaseViewSerializer.Meta.fields + (
            'projects_count',
        )
        validators = (
            ViewUniqueURIValidator(),
            ViewLockedValidator()
        )


class ViewListSerializer(ElementExportSerializerMixin, ElementWarningSerializerMixin,
                         BaseViewSerializer):

    warning = serializers.SerializerMethodField()
    xml_url = serializers.SerializerMethodField()

    class Meta(BaseViewSerializer.Meta):
        fields = BaseViewSerializer.Meta.fields + (
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
