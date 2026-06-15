from django.db import models
from django.utils.translation import gettext_lazy as _


class RelationTypes(models.TextChoices):
    RELATION_EQUAL = 'eq', _('is equal to (==)')
    RELATION_NOT_EQUAL = 'neq', _('is not equal to (!=)')
    RELATION_CONTAINS = 'contains', _('contains')
    RELATION_GREATER_THAN = 'gt', _('is greater than (>)')
    RELATION_GREATER_THAN_EQUAL = 'gte', _('is greater than or equal (>=)')
    RELATION_LESS_THAN = 'lt', _('is less than (<)')
    RELATION_LESS_THAN_EQUAL = 'lte', _('is less than or equal (<=)')
    RELATION_EMPTY = 'empty', _('is empty')
    RELATION_NOT_EMPTY = 'notempty', _('is not empty')
