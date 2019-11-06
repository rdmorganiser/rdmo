from django.db import models
from rdmo.core.managers import (CurrentSiteManagerMixin,
                                CurrentSiteQuerySetMixin, GroupsQuerySetMixin)


class TaskQuestionSet(CurrentSiteQuerySetMixin, GroupsQuerySetMixin, models.QuerySet):

    def filter_catalog(self, catalog):
        return self.filter(models.Q(catalogs=None) | models.Q(catalogs=catalog))


class TaskManager(CurrentSiteManagerMixin, CurrentSiteQuerySetMixin, models.Manager):

    def get_queryset(self):
        return TaskQuestionSet(self.model, using=self._db)

    def filter_catalog(self, catalog):
        return self.get_queryset().filter_catalog(catalog)

    def active(self, project):
        tasks = []
        for task in self:
            conditions = task.conditions.all()

            if conditions:
                for condition in conditions:
                    if condition.resolve(project):
                        tasks.append(task)
                        break

                task.dates = task.get_dates(project.values.filter(snapshot=None))

        return tasks
