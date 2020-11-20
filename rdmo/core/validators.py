from django.apps import apps
from django.core.exceptions import (MultipleObjectsReturned,
                                    ObjectDoesNotExist, ValidationError)
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class UniqueURIValidator(object):

    def __init__(self, instance=None):
        self.instance = instance

    def set_context(self, serializer):
        self.instance = serializer.instance

    def validate(self, data=None):
        model = apps.get_model(app_label=self.app_label, model_name=self.model_name)

        if data is None:
            # the validator is used on an existing instance
            uri = self.instance.uri
        else:
            # get the uri using the specific get_uri method
            uri = self.get_uri(model, data)

        try:
            if self.instance:
                model.objects.exclude(pk=self.instance.pk).get(uri=uri)
            else:
                model.objects.get(uri=uri)
        except ObjectDoesNotExist:
            return
        except MultipleObjectsReturned:
            pass

        raise ValidationError({
            'key': _('%(model)s with the uri "%(uri)s" already exists.') % {
                'model': model._meta.verbose_name.title(),
                'uri': uri
            }
        })

    def get_uri(self, model, data):
        raise NotImplementedError

    def __call__(self, data=None):
        try:
            self.validate(data)
        except ValidationError as e:
            errors = {key: value for key, value in e.message_dict.items()}
            raise serializers.ValidationError(errors)
