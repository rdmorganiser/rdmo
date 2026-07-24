from django.utils.translation import gettext_lazy as _

from rdmo.core.validators import InstanceValidator, LockedValidator, UniqueURIValidator

from .models import Attribute


class AttributeUniqueURIValidator(UniqueURIValidator):

    model = Attribute

    def get_uri(self, data, instance, serializer):
        key = self.get_value(data, instance, 'key')
        parent = self.get_value(data, instance, 'parent')
        uri_prefix = self.get_value(data, instance, 'uri_prefix')

        if not key:
            self.raise_validation_error({'key': _('This field is required.')}, serializer)
        else:
            if parent is None:
                # workaround for import
                parent_id = data.get('parent_id')
                if parent_id:
                    parent = self.model.objects.filter(id=parent_id).first()
                    if parent is None:
                        self.raise_validation_error({'parent': [_('The parent does not exist.')]}, serializer)

            path = self.model.build_path(key, parent)
            uri = self.model.build_uri(uri_prefix, path)
            return uri


class AttributeParentValidator(InstanceValidator):

    def __call__(self, data, serializer=None):
        instance = self.get_instance(serializer)

        parent = data.get('parent')
        if parent is None:
            # workaround for import
            parent_id = data.get('parent_id')
            if parent_id:
                parent = Attribute.objects.filter(id=parent_id).first()
                if parent is None:
                    self.raise_validation_error({'parent': [_('The parent does not exist.')]}, serializer)

        if parent:
            if serializer is not None:
                # check copied attributes
                view = serializer.context.get('view')
                if view and getattr(view, 'action', None) == 'copy':
                    # get the original from the view when cloning an attribute
                    if parent in view.get_object().get_descendants(include_self=True):
                        self.raise_validation_error({
                            'parent': [
                                _('An attribute may not be cloned to be a child of itself or one of its descendants.')
                            ]
                        }, serializer)

            # only check updated attributes
            if instance is not None and instance.pk:
                if parent in instance.get_descendants(include_self=True):
                    self.raise_validation_error({
                        'parent': [
                            _('An attribute may not be moved to be a child of itself or one of its descendants.')
                        ]
                    }, serializer)


class AttributeLockedValidator(LockedValidator):

    parent_fields = ('parent', )
