import logging
from pathlib import Path

from django.conf import settings
from django.contrib.sites.models import Site
from django.db import connection
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.timezone import now

from rdmo.core.mail import send_mail
from rdmo.core.plugins import get_plugins

logger = logging.getLogger(__name__)


def get_value_path(project, snapshot=None):
    if snapshot is None:
        return Path('projects') / str(project.id) / 'values'
    else:
        return Path('projects') / str(project.id) / 'snapshots' / str(snapshot.id) / 'values'


def is_last_owner(project, user):
    # check if user is owner
    if user in project.owners:
        # check if the user is the last owner
        return project.owners.count() <= 1
    else:
        return False


def check_conditions(conditions, values, set_prefix=None, set_index=None):
    if conditions:
        for condition in conditions:
            if condition.resolve(values, set_prefix, set_index):
                return True
        return False
    else:
        return True


def copy_project(project, site, owners):
    from .models import Membership, Value  # to prevent circular inclusion

    timestamp = now()

    tasks = project.tasks.all()
    views = project.views.all()

    values = project.values.filter(snapshot=None)
    snapshots = {
        snapshot: project.values.filter(snapshot=snapshot)
        for snapshot in project.snapshots.all()
    }

    # create a temporary buffer for all values with files
    file_values = []

    # unset the id, set current site and update timestamps
    project.id = None
    project.site = site
    project.created = timestamp

    # save the new project
    project.save()

    # save project tasks
    for task in tasks:
        project.tasks.add(task)

    # save project views
    for view in views:
        project.views.add(view)

    # save current project values
    project_values = []
    for value in values:
        value.id = None
        value.project = project
        value.created = timestamp

        if value.file:
            file_values.append((value, value.file_name, value.file))

        project_values.append(value)

    # insert the new values using bulk_create
    Value.objects.bulk_create(project_values)

    # save project snapshots
    for snapshot, snapshot_values in snapshots.items():
        snapshot.id = None
        snapshot.project = project
        snapshot.created = timestamp
        snapshot.save(copy_values=False)

        project_snapshot_values = []
        for value in snapshot_values:
            value.id = None
            value.project = project
            value.snapshot = snapshot
            value.created = timestamp

            if value.file:
                file_values.append((value, value.file_name, value.file))

            project_snapshot_values.append(value)

        # insert the new snapshot values using bulk_create
        Value.objects.bulk_create(project_snapshot_values)

    for value, file_name, file_content in file_values:
        if connection.vendor == 'postgres':
            # bulk_create will only set the primary key on cool databases
            # https://docs.djangoproject.com/en/4.2/ref/models/querysets/#bulk-create
            value.copy_file(file_name, file_content)
        else:
            # refetch the value from the database, we use filter and first here to be more
            # stable against weird cases, where collection_index is not unique
            db_value = Value.objects.filter(
                project=value.project,
                snapshot=value.snapshot,
                attribute=value.attribute,
                set_prefix=value.set_prefix,
                set_index=value.set_index,
                collection_index=value.collection_index
            ).first()
            if db_value and db_value.file_name == file_name:
                db_value.copy_file(file_name, file_content)

    for owner in owners:
        membership = Membership(project=project, user=owner, role='owner')
        membership.save()

    return project


def save_import_values(project, values, checked):
    for value in values:
        if value.attribute:
            value_key = f'{value.attribute.uri}[{value.set_prefix}][{value.set_index}][{value.collection_index}]'

            if value_key in checked:
                current_value = value.current
                if current_value is None:
                    # assert that this is a new value
                    assert value.pk is None

                    value.project = project
                    value.save()

                    if value.file:
                        value.copy_file(value.file_name, value.file)
                    else:
                        try:
                            name = value.file_import.get('name')
                            file = value.file_import.get('file')
                            value.file.save(name, file)
                        except AttributeError:
                            pass

                else:
                    # make sure we have the correct value
                    assert current_value.snapshot is None
                    assert current_value.attribute == value.attribute
                    assert current_value.set_prefix == value.set_prefix
                    assert current_value.set_index == value.set_index
                    assert current_value.collection_index == value.collection_index

                    # assert that this is an new value
                    assert current_value.pk is not None

                    current_value.text = value.text
                    current_value.option = value.option
                    current_value.value_type = value.value_type
                    current_value.unit = value.unit
                    current_value.save()

                    if value.file:
                        current_value.file.delete()
                        current_value.copy_file(value.file_name, value.file)
                    else:
                        try:
                            name = value.file_import.get('name')
                            file = value.file_import.get('file')
                            current_value.file.delete()
                            current_value.file.save(name, file)
                        except AttributeError:
                            pass


def save_import_snapshot_values(project, snapshots, checked):
    for snapshot in snapshots:
        # assert that this is a new snapshot
        assert snapshot.pk is None

        snapshot.project = project
        snapshot.save(copy_values=False)

        for value in snapshot.snapshot_values:
            if value.attribute:
                value_key = f"{value.attribute.uri}[{snapshot.snapshot_index}][{value.set_prefix}][{value.set_index}][{value.collection_index}]" # noqa: E501

                if value_key in checked:
                    # assert that this is a new value
                    assert value.pk is None

                    value.project = project
                    value.snapshot = snapshot
                    value.save()

                    if value.file:
                        value.copy_file(value.file_name, value.file)
                    else:
                        try:
                            name = value.file_import.get('name')
                            file = value.file_import.get('file')
                            value.file.save(name, file)
                        except AttributeError:
                            pass


def save_import_tasks(project, tasks):
    for task in tasks:
        project.tasks.add(task)


def save_import_views(project, views):
    for view in views:
        project.views.add(view)


def get_invite_email_project_path(invite) -> str:
    project_invite_path = reverse('project_join', args=[invite.token])
    # check if the invited user exists and the multisite environment is enabled
    if invite.user is not None and settings.MULTISITE:
        # do nothing if user is a member of the current site
        current_site = Site.objects.get_current()
        if not invite.user.role.member.filter(id=current_site.id).exists():
            # else take first site
            invited_user_member_domain = invite.user.role.member.first().domain
            project_invite_path = 'http://' + invited_user_member_domain + project_invite_path
    return project_invite_path


def send_invite_email(request, invite):
    project_invite_path = get_invite_email_project_path(invite)
    context = {
        'invite_url': request.build_absolute_uri(project_invite_path),
        'invite_user': invite.user,
        'invite_email': invite.email,
        'project': invite.project,
        'user': request.user,
        'site': Site.objects.get_current()
    }

    subject = render_to_string('projects/email/project_invite_subject.txt', context)
    message = render_to_string('projects/email/project_invite_message.txt', context)

    # send the email
    send_mail(subject, message, to=[invite.email])


def set_context_querystring_with_filter_and_page(context: dict) -> dict:
    '''prepares the filter part of the querystring for the next and previous hyperlinks in the pagination'''
    if context["filter"].data:
        querystring = context["filter"].data.copy()
        if context["filter"].data.get('page'):
            del querystring['page']
        context['querystring'] = querystring.urlencode()
    return context


def get_upload_accept():
    accept = set()
    for import_plugin in get_plugins('PROJECT_IMPORTS').values():
        if import_plugin.accept:
            accept.add(import_plugin.accept)
        else:
            return None
    return ','.join(accept)
