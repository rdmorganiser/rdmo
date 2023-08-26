import re

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist, ValidationError
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class InstanceValidator:

    '''
    BaseValidator which should work with model instances, used by

    1) the DRF serializer (having self.serializer)
    2) the form clean method through the admin interface

    It is used as InstanceValidator() for (1) and InstanceValidator(instance)(self.cleaned_data) for (2)
    '''

    requires_context = True

    def __init__(self, instance=None):
        self.instance = instance
        self.serializer = None

    def __call__(self, data, serializer=None):
        if serializer is not None:
            self.instance = serializer.instance
            self.serializer = serializer

    def raise_validation_error(self, errors):
        if self.serializer:
            raise serializers.ValidationError(errors)
        else:
            raise ValidationError(errors)


class UniqueURIValidator(InstanceValidator):

    model = None
    models = []

    path_pattern = re.compile(r'^[\w\-\/]+\Z')

    def __call__(self, data, serializer=None):
        super().__call__(data, serializer)

        self.validate(self.model, self.instance, self.get_uri(data))

    def validate(self, model, instance, uri):
        models = self.models or [model]

        for model in models:
            try:
                if instance:
                    model.objects.exclude(pk=instance.id).get(uri=uri)
                else:
                    model.objects.get(uri=uri)
            except MultipleObjectsReturned:
                pass
            except ObjectDoesNotExist:
                continue

            message = _('%(model)s with the uri "%(uri)s" already exists.') % {
                'model': model._meta.verbose_name.title(),
                'uri': uri
            }

            self.raise_validation_error({
                'uri_path': message,
                'key': message
            })

    def get_uri(self, data):
        uri_prefix = data.get('uri_prefix')
        uri_path = data.get('uri_path')

        if not uri_path:
            self.raise_validation_error({
                'uri_path': _('This field is required.')
            })
        elif not self.path_pattern.match(uri_path):
            self.raise_validation_error({
                'uri_path': _('This value may contain only letters, numbers, slashes, hyphens and underscores.')
            })
        else:
            uri = self.model.build_uri(uri_prefix, uri_path)
            return uri


class LockedValidator(InstanceValidator):

    parent_fields = ()

    def __call__(self, data, serializer=None):
        super().__call__(data, serializer)

        is_locked = False

        # lock if parent_fields are set and a parent is locked
        for parent_field in self.parent_fields:
            parent = data.get(parent_field)
            try:
                is_locked |= parent.is_locked
            except AttributeError:
                try:
                    for p in parent:
                        is_locked |= p.is_locked
                except TypeError:
                    pass

        if self.instance:
            # lock if the instance itself has locked parents
            for parent_field in self.parent_fields:
                parent = getattr(self.instance, parent_field)

                try:
                    is_locked |= parent.is_locked
                except AttributeError:
                    try:
                        for p in parent.all():
                            is_locked |= p.is_locked
                    except AttributeError:
                        pass

        # lock if a superior element is locked
        if is_locked:
            raise self.raise_validation_error({
                'locked': _('A superior element is locked.')
            })

        # lock if the instance is now locked and was locked before
        if data.get('locked', False) and self.instance and self.instance.locked:
            if data.get('locked'):
                raise self.raise_validation_error({
                    'locked': _('The element is locked.')
                })
