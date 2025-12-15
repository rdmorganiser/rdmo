from django.db.models import Manager, QuerySet

from rdmo.core.managers import AvailabilityQuerySetMixin


class ViewQuerySet(AvailabilityQuerySetMixin, QuerySet):
    pass

class ViewManager(Manager):

    def get_queryset(self) -> ViewQuerySet:
        return ViewQuerySet(self.model, using=self._db)

    def filter_availability(self, user) -> QuerySet:
        return self.get_queryset().filter_availability(user)
