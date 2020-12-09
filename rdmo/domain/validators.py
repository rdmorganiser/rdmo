from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from rdmo.core.validators import UniqueURIValidator


class AttributeUniqueURIValidator(UniqueURIValidator):

    app_label = 'domain'
    model_name = 'attribute'

    def get_uri(self, model, data):
        path = model.build_path(data.get('key'), data.get('parent'))
        uri = model.build_uri(data.get('uri_prefix'), path)
        return uri


class AttributeParentValidator(UniqueURIValidator):

    requires_context = True

    def __call__(self, data, serializer):
        if self.instance is None:
            try:
                # get the original from the view when cloning an attribute
                original = serializer.context['view'].get_object()
                if data.get('parent') in original.get_descendants(include_self=True):
                    raise serializers.ValidationError({
                        'parent': [_('An attribute may not be cloned to be a child of itself or one of its descendants.')]
                    })
            except AssertionError:
                pass
        else:
            if data.get('parent') in self.instance.get_descendants(include_self=True):
                raise serializers.ValidationError({
                    'parent': [_('An attribute may not be moved to be a child of itself or one of its descendants.')]
                })
