from django.apps import apps
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

# from rest_framework import serializers


def unique_uri_model_validator(instance):
    try:
        instance.__class__.objects.exclude(pk=instance.pk).get(uri=instance.uri)
        raise ValidationError(_('The URI %s is already taken. Please adjust the URI Prefix and/or the Key.' % instance.uri))
    except ObjectDoesNotExist:
        pass


class UniqueLabelSerializerValidator(object):

    def set_context(self, serializer):
        self.instance = serializer.instance

    def __call__(self, data):
        Model = self.get_model()
        label = self.get_label(data)

        print label

        try:
            if self.instance:
                Model.objects.exclude(pk=self.instance.pk).get(label=label)
            else:
                Model.objects.get(label=label)

            raise ValidationError(_('Another %(model)s with the label "%(label)s" already exists. Please adjust the the Key.') % {
                    'model': Model._meta.verbose_name.title(),
                    'label': label
            })
        except ObjectDoesNotExist:
            pass
