from django.template import Template, TemplateSyntaxError, Context

from rest_framework import serializers
from rest_framework import exceptions

from rdmo.core.serializers import TranslationSerializerMixin
from rdmo.core.utils import get_language_warning

from ..models import View
from ..validators import ViewUniqueKeyValidator


class ViewIndexSerializer(serializers.ModelSerializer):

    warning = serializers.SerializerMethodField()

    class Meta:
        model = View
        fields = (
            'id',
            'key',
            'comment',
            'title',
            'help',
            'warning'
        )

    def get_warning(self, obj):
        return get_language_warning(obj, 'title')


class ViewSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    key = serializers.CharField(required=True)

    def validate(self, data):
        # try to render the tamplate to see that the syntax is ok
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
            'uri_prefix',
            'key',
            'comment',
            'template'
        )
        trans_fields = (
            'title',
            'help'
        )
        validators = (ViewUniqueKeyValidator(), )
