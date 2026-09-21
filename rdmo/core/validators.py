import re

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist, ValidationError
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class InstanceValidator:

    '''
    BaseValidator which should work with model instances, used by

    1) the DRF serializer (providing serializer to __call__)
    2) the form clean method through the admin interface (providing instance to __init__)

    It is used as InstanceValidator() for (1) and InstanceValidator(instance)(self.cleaned_data) for (2)
    '''

    requires_context = True

    def __init__(self, instance=None):
        # admin interface case, where a fresh validator is built per call
        self.instance = instance

    def __call__(self, data, serializer=None):
        raise NotImplementedError

    def get_instance(self, serializer):
        if serializer is not None:
            return serializer.instance
        return self.instance

    def get_value(self, data, instance, field):
        if field in data:
            return data[field]
        return getattr(instance, field, None)

    def raise_validation_error(self, errors, serializer=None):
        if serializer is not None:
            raise serializers.ValidationError(errors)
        raise ValidationError(errors)


class UniqueURIValidator(InstanceValidator):

    model = None
    models = []

    path_pattern = re.compile(r'^[\w\-\/]+\Z')

    def __call__(self, data, serializer=None):
        models = self.models or [self.model]
        instance = self.get_instance(serializer)

        uri = self.get_uri(data, instance, serializer)

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
            }, serializer)

    def get_uri(self, data, instance, serializer):
        uri_prefix = self.get_value(data, instance, 'uri_prefix')
        uri_path = self.get_value(data, instance, 'uri_path')

        if not uri_path:
            self.raise_validation_error({
                'uri_path': _('This field is required.')
            }, serializer)
        elif not self.path_pattern.match(uri_path):
            self.raise_validation_error({
                'uri_path': _('This value may contain only letters, numbers, slashes, hyphens and underscores.')
            }, serializer)
        else:
            uri = self.model.build_uri(uri_prefix, uri_path)
            return uri


class LockedValidator(InstanceValidator):

    parent_fields = ()

    def __call__(self, data, serializer=None):
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

        instance = self.get_instance(serializer)
        if instance:
            # lock if the instance itself has locked parents
            for parent_field in self.parent_fields:
                parent = getattr(instance, parent_field)

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
            self.raise_validation_error({
                'locked': _('A superior element is locked.')
            }, serializer)

        # lock if the instance is now locked and was locked before
        locked = self.get_value(data, instance, 'locked')
        if locked and instance is not None and instance.locked:
            self.raise_validation_error({
                'locked': _('The element is locked.')
            }, serializer)
