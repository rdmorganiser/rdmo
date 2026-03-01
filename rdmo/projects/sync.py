import logging

from django.conf import settings
from django.db.models import Exists, OuterRef, Q

from rdmo.tasks.models import Task
from rdmo.views.models import View

from .models import Membership, Project

logger = logging.getLogger(__name__)


def sync_task_or_view_to_projects(instance):
    # get the m2m field for the Project model
    if isinstance(instance, Task):
        field = 'tasks'
    elif isinstance(instance, View):
        field = 'views'
    else:
        raise RuntimeError('instance needs to be a Task or View')

    target_projects = filter_projects_for_task_or_view(instance)
    current_projects = Project.objects.filter(**{field: instance})

    to_remove = current_projects.exclude(pk__in=target_projects)
    to_add = target_projects.exclude(pk__in=current_projects)

    if not to_remove and not to_add:
        logger.debug(
            'No projects to change for %s(id=%s)', type(instance).__name__, instance.id
        )
        return

    if to_remove:
        logger.debug(
            'Removing %s(id=%s) from Projects: %s', type(instance).__name__, instance.id, [p.id for p in to_remove]
        )
        instance.projects.remove(*to_remove)

    if to_add:
        logger.debug(
            'Adding %s(id=%s) to Projects: %s', type(instance).__name__, instance.id, [p.id for p in to_add]
        )
        instance.projects.add(*to_add)


def sync_tasks_or_views_for_project(model, project):
    # get the m2m field for the Project model
    if model == Task:
        field = 'tasks'
    elif model == View:
        field = 'views'
    else:
        raise RuntimeError('model needs to be Task or View')

    desired_instances = filter_tasks_or_views_for_project(model, project)
    current_instances = getattr(project, field).all()

    to_remove = current_instances.exclude(pk__in=desired_instances)
    to_add = desired_instances.exclude(pk__in=current_instances)

    if not to_remove and not to_add:
        logger.debug(
            'No %s to change for Project(id=%s)', model, project.id
        )
        return

    if to_remove:
        logger.debug(
            'Removing %s %s from Project(id=%s)', model, [i.id for i in to_remove], project.id
        )
        getattr(project, field).remove(*to_remove)

    if to_add:
        logger.debug(
            'Adding %s %s to Project(id=%s)', model, [i.id for i in to_add], project.id
        )
        getattr(project, field).add(*to_add)


def filter_tasks_or_views_for_project(model, project):
    # get eiter tasks.view_task or views.view_view
    permission = f'{model._meta.app_label}.view_{model._meta.model_name}'

    # get all tasks/views which have no catalog/group or the catalog/group of the project
    queryset = (
        model.objects.filter(Q(catalogs=None) | Q(catalogs=project.catalog))
                     .filter(Q(groups=None) | Q(groups__in=project.groups))
    )

    # check if all members of the project have tasks.view_task/views.view_view
    memberships = project.memberships.all()
    if memberships and all(
        membership.user.has_perm(permission) for membership in memberships
    ):
        # if all users have model permissions, tasks/views do not need to be checked for availability
        pass
    else:
        queryset = queryset.filter(available=True)

    if settings.MULTISITE:
        return queryset.filter(sites=project.site)
    else:
        return queryset.filter(Q(sites=None) | Q(sites=project.site))


def filter_projects_for_task_or_view(instance):
    queryset = Project.objects

    if not instance.available:
        # perform a subquery to check if the project has any users which do not have
        # the view permission for the instance
        users_without_permissions_subquery = (
            Membership.objects.filter(project_id=OuterRef('pk')).exclude(
                Q(user__is_superuser=True) |
                Q(user__groups__permissions__content_type__app_label=instance._meta.app_label,
                  user__groups__permissions__codename=f'view_{instance._meta.model_name}') |
                Q(user__role__editor=OuterRef('site_id')) |
                Q(user__role__reviewer=OuterRef('site_id'))
            )
        )

        queryset = (
            queryset.exclude(memberships=None)
                    .annotate(has_users_without_permissions=Exists(users_without_permissions_subquery))
                    .exclude(has_users_without_permissions=True)
        )

    # when View/Task has any catalogs it can be filtered for those
    if instance.catalogs.exists():
        queryset = queryset.filter(catalog__in=instance.catalogs.all())

    # when View/Task has any sites it can be filtered for those
    if instance.sites.exists():
        queryset = queryset.filter(site__in=instance.sites.all())
    elif settings.MULTISITE:
        # when View/Task has no sites in a multi-site, it should not appear at all
        return queryset.none()

    # when  has any groups it can be filtered for those
    if instance.groups.exists():
        queryset = queryset.filter_groups(instance.groups.all())

    return queryset.all()
