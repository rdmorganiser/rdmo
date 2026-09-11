import logging

from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.utils.translation import get_language, get_supported_language_variant
from django.utils.translation import gettext_lazy as _

from treebeard.ns_tree import NS_Node

from rdmo.core.utils import get_languages

logger = logging.getLogger(__name__)


class Model(models.Model):

    created = models.DateTimeField(editable=False, verbose_name=_('created'))
    updated = models.DateTimeField(editable=False, verbose_name=_('updated'))

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.created is None:
            self.created = now()

        self.updated = now()

        super().save(*args, **kwargs)


class TreeModel(NS_Node):

    parent = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.DO_NOTHING, related_name='children', db_index=True,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.lft is None or self.rgt is None:
            if self.parent is None:
                self.__class__.objects.add_root(instance=self)
            else:
                self.__class__.objects.add_child(self.parent, instance=self)
        else:
            super().save(*args, **kwargs)

            cached_parent = self._meta.get_field("parent").get_cached_value(self)
            if self.parent != cached_parent:
                if self.parent is None:
                    a_root_node = self.__class__.objects.get_root_nodes()[0]
                    self.__class__.objects.move(self, a_root_node, pos="last-sibling")
                else:
                    self.__class__.objects.move(self, self.parent, pos="last-child")

    def full_clean(self, exclude=("lft", "rgt", "tree_id", "depth"), validate_unique=True, validate_constraints=True):
        super().full_clean(exclude=exclude, validate_unique=validate_unique, validate_constraints=validate_constraints)


class TranslationMixin:

    def trans(self, field):
        current_language = get_supported_language_variant(get_language())

        languages = get_languages()
        for lang_code, _lang_string, lang_field in languages:
            if lang_code == current_language:
                r = getattr(self, f'{field}_{lang_field}') or None
                if r is not None:
                    return r
                elif settings.REPLACE_MISSING_TRANSLATION:
                    for i in range(1, 6):
                        r = getattr(self, '{}_{}'.format(field, 'lang' + str(i))) or None
                        if r is not None:
                            return r
        return ''
