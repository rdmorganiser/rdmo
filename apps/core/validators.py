from django.apps import apps
from django.core.exceptions import ValidationError, ObjectDoesNotExist, MultipleObjectsReturned
from django.utils.translation import ugettext_lazy as _


class UniquePathValidator(object):

    def __init__(self, instance=None):
        self.instance = instance

    def set_context(self, serializer):
        self.instance = serializer.instance

    def __call__(self, data=None):
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

        raise ValidationError(_('Another %(model)s with the path "%(path)s" already exists. Please adjust the the Key.') % {
                'model': model._meta.verbose_name.title(),
                'path': path
        })
