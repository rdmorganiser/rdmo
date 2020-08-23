from django.template import Context, Template, TemplateSyntaxError
from rdmo.core.serializers import SiteSerializer, TranslationSerializerMixin
from rdmo.core.utils import get_language_warning
from rest_framework import exceptions, serializers
from rest_framework.reverse import reverse

from ..models import View
from ..validators import ViewUniqueKeyValidator


class ViewSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

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
            'uri',
            'uri_prefix',
            'key',
            'comment',
            'available',
            'catalogs',
            'sites',
            'groups',
            'template'
        )
        trans_fields = (
            'title',
            'help'
        )
        validators = (ViewUniqueKeyValidator(), )


class ViewIndexSerializer(serializers.ModelSerializer):

    sites = SiteSerializer(many=True, read_only=True)
    warning = serializers.SerializerMethodField()
    xml_url = serializers.SerializerMethodField()

    class Meta:
        model = View
        fields = (
            'id',
            'uri_prefix',
            'uri',
            'key',
            'available',
            'sites',
            'title',
            'help',
            'warning',
            'xml_url'
        )

    def get_warning(self, obj):
        return get_language_warning(obj, 'title')

    def get_xml_url(self, obj):
        return reverse('v1-views:view-detail-export', args=[obj.pk])
