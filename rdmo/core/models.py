from django.db import models
from django.utils.timezone import now
from django.utils.translation import get_language
from django.utils.translation import ugettext_lazy as _
from rdmo.core.utils import get_languages


class Model(models.Model):

    created = models.DateTimeField(editable=False, verbose_name=_('created'))
    updated = models.DateTimeField(editable=False, verbose_name=_('updated'))

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.created is None:
            self.created = now()

        self.updated = now()

        super(Model, self).save(*args, **kwargs)


class TranslationMixin(object):

    def trans(self, field):
        current_language = get_language()

        languages = get_languages()
        for lang_code, lang_string, lang_field in languages:
            if lang_code == current_language:
                return getattr(self, '%s_%s' % (field, lang_field)) or ''

        primary_lang_field = languages[0][2]
        return getattr(self, '%s_%s' % (field, primary_lang_field)) or ''
