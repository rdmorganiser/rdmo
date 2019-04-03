from django.apps import apps
from django.core.exceptions import (MultipleObjectsReturned,
                                    ObjectDoesNotExist, ValidationError)
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class UniqueKeyValidator(object):

    def __init__(self, instance=None):
        self.instance = instance

    def set_context(self, serializer):
        self.instance = serializer.instance

    def validate(self, data=None):
        model = apps.get_model(app_label=self.app_label, model_name=self.model_name)

        if data is None:
            # the validator is used on an existing instance
            key = self.instance.key
        else:
            # the validator is used on a data dict
            key = self.get_key(data)

        try:
            if self.instance:
                model.objects.exclude(pk=self.instance.pk).get(key=key)
            else:
                model.objects.get(key=key)
        except ObjectDoesNotExist:
            return
        except MultipleObjectsReturned:
            pass

        raise ValidationError({
            'key': _('%(model)s with this key already exists.') % {
                'model': model._meta.verbose_name.title()
            }
        })

    def get_key(self, data):
        if 'key' in data:
            key = data['key']
        else:
            raise ValidationError({
                'key': _('This field is required')
            })

    def __call__(self, data=None):
        try:
            self.validate(data)
        except ValidationError as e:
            raise serializers.ValidationError({
                'key': e.message_dict['key']
            })



class UniquePathValidator(object):

    def __init__(self, instance=None):
        self.instance = instance

    def set_context(self, serializer):
        self.instance = serializer.instance

    def validate(self, data=None):
        model = apps.get_model(app_label=self.app_label, model_name=self.model_name)

        if data is None:
            # the validator is used on an existing instance
            path = self.instance.path
        else:
            # the validator is used on a data dict
            path = self.get_path(model, data)

        try:
            if self.instance:
                model.objects.exclude(pk=self.instance.pk).get(path=path)
            else:
                model.objects.get(path=path)
        except ObjectDoesNotExist:
            return
        except MultipleObjectsReturned:
            pass

        raise ValidationError({
            'key': _('%(model)s with the path "%(path)s" already exists. Please adjust the the Key.') % {
                'model': model._meta.verbose_name.title(),
                'path': path
            }
        })

    def get_path(self, model, data):
        raise NotImplementedError

    def __call__(self, data=None):
        try:
            self.validate(data)
        except ValidationError as e:
            errors = {key: value for key, value in e.message_dict.items()}
            raise serializers.ValidationError(errors)
