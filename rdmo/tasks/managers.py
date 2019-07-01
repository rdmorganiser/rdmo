from django.contrib.sites.managers import CurrentSiteManager
from django.db.models import Q


class TaskManager(CurrentSiteManager):

    def active(self, user, project):
        groups = user.groups.all()
        queryset = super().filter(Q(groups=None) | Q(groups__in=groups))

        tasks = []

        for task in queryset:
            conditions = task.conditions.all()

            if conditions:
                for condition in conditions:
                    if condition.resolve(project):
                        tasks.append(task)
                        break

                task.dates = task.get_dates(project)

        return tasks
