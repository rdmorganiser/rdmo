from django.db.models import Manager, QuerySet

from rdmo.core.managers import AvailabilityQuerySetMixin


class TaskQuerySet(AvailabilityQuerySetMixin, QuerySet):
    pass

class TaskManager(Manager):

    def get_queryset(self) -> TaskQuerySet:
        return TaskQuerySet(self.model, using=self._db)

    def filter_availability(self, user) -> QuerySet:
        return self.get_queryset().filter_availability(user)
