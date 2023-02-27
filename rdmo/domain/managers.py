from django.db import models

from mptt.models import TreeManager
from mptt.querysets import TreeQuerySet
from mptt.models import MPTTModel
from rdmo.core.managers import EditableElementQuerySetMixin, EditableElementManagerMixin

class AttributeQuerySet(EditableElementQuerySetMixin, TreeQuerySet):
    pass

class AttributeManager(EditableElementManagerMixin, TreeManager):

    def get_queryset(self):
        return AttributeQuerySet(self.model, using=self._db)
