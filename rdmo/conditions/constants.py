from django.db import models
from django.utils.translation import gettext_lazy as _


class RelationTypes(models.TextChoices):
    RELATION_EQUAL = 'eq', _('is equal to (==)')
    RELATION_NOT_EQUAL = 'neq', _('is not equal to (!=)')
    RELATION_CONTAINS = 'contains', _('contains')
    RELATION_GREATER_THAN = 'gt', _('is greater than (>)')
    RELATION_GREATER_THAN_EQUAL = 'gte', _('is greater than or equal (>=)')
    RELATION_LESSER_THAN = 'lt', _('is lesser than (<)')
    RELATION_LESSER_THAN_EQUAL = 'lte', _('is lesser than or equal (<=)')
    RELATION_EMPTY = 'empty', _('is empty')
    RELATION_NOT_EMPTY = 'notempty', _('is not empty')
