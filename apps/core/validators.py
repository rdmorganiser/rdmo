from django.apps import apps
from django.core.exceptions import ValidationError, ObjectDoesNotExist, MultipleObjectsReturned
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
            key = self.instance.key
        else:
            if 'key' in data and data['key']:
                key = data['key']
            else:
                raise ValidationError({
                    'key': _('This field may not be blank.')
                })

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

    def __call__(self, data=None):
        try:
            self.validate(data)
        except ValidationError as e:
            raise serializers.ValidationError({
                'key': e.error_dict['key'][0][0]
            })


class UniquePathValidator(object):

    def __init__(self, instance=None):
        self.instance = instance

    def set_context(self, serializer):
        self.instance = serializer.instance

    def validate(self, data=None):
        model = apps.get_model(app_label=self.app_label, model_name=self.model_name)

        if data:
            path = self.get_path(model, data)
        else:
            path = self.instance.path

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

    def __call__(self, data=None):
        try:
            self.validate(data)
        except ValidationError as e:
            raise serializers.ValidationError({
                'key': e.error_dict['key'][0][0]
            })
