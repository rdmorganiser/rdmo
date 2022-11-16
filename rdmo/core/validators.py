from django.core.exceptions import (MultipleObjectsReturned,
                                    ObjectDoesNotExist, ValidationError)
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class InstanceValidator(object):

    '''
    BaseValidator which should work with model instances, used by

    1) the DRF serializer (having self.serializer)
    2) the form clean method through the admin interface

    It is used as InstanceValidator() for (1) and InstanceValidator(instance)(self.cleaned_data) for (2)
    '''

    def __init__(self, instance=None):
        self.instance = instance
        self.serializer = None

    def set_context(self, serializer):
        self.instance = serializer.instance
        self.serializer = serializer

    def raise_validation_error(self, errors):
        if self.serializer:
            raise serializers.ValidationError(errors)
        else:
            raise ValidationError(errors)

    def __call__(self, value):
        raise NotImplementedError


class UniqueURIValidator(InstanceValidator):

    model = None

    def __call__(self, data):
        self.validate(self.model, self.instance, self.get_uri(data))

    def validate(self, model, instance, uri):
        try:
            if instance:
                model.objects.exclude(pk=instance.id).get(uri=uri)
            else:
                model.objects.get(uri=uri)
        except MultipleObjectsReturned:
            pass
        except ObjectDoesNotExist:
            return

        self.raise_validation_error({
            'key': _('%(model)s with the uri "%(uri)s" already exists.') % {
                'model': model._meta.verbose_name.title(),
                'uri': uri
            }
        })

    def get_uri(self, data):
        raise NotImplementedError


class LockedValidator(InstanceValidator):

    parent_field = None

    def __call__(self, data):
        is_locked = False
        # lock if a parent_field is set and a parent is set and the parent is locked
        if self.parent_field:
            parent = data.get(self.parent_field)
            if parent:
                is_locked |= parent.is_locked

        # lock only if the instance is now locked and was locked before
        if self.instance:
            is_locked |= data.get('locked', False) and self.instance.is_locked
        # compare the content_editor sites of the user with the editor_sites of the instance
        if not is_locked:
            if self.serializer:
                instance_editable_by_user = is_editable_by_user(self.instance, self.serializer.context['request']._user)
                if not instance_editable_by_user:
                    is_locked = True
            
        if is_locked:
            if data.get('locked'):
                raise self.raise_validation_error({
                    'locked': _('The element is locked.')
                })
            else:
                raise self.raise_validation_error({
                    'locked': _('A superior element is locked.')
                })
                
def is_editable_by_user(obj, user) -> bool:
    ''' checks permission for the given object and user '''

    if not hasattr(obj, 'editor_sites'):
        # no editor_sites on object, so no locking (during development)
        return True

    if not user.role.content_editor.all().exists():
        # user has no content_editor rights
        return False

    obj_editable_by_sites = obj.editor_sites.all()
    user_role_editor_sites = user.role.content_editor.all()
    obj_editable_by_user = user_role_editor_sites.filter(id__in=obj_editable_by_sites).exists()

    return obj_editable_by_user
