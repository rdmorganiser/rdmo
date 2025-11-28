from django.db.models import Manager

from rdmo.management.managers import ForProjectManagerMixin


class ViewManager(ForProjectManagerMixin, Manager):
    pass
