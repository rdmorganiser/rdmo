import logging
from pathlib import Path

from django.conf import settings
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.urls import reverse

from rdmo.core.mail import send_mail

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
                value_key = '{value.attribute.uri}[{snapshot_index}][{value.set_prefix}][{value.set_index}][{value.collection_index}]'.format(  # noqa: E501
                    value=value,
                    snapshot_index=snapshot.snapshot_index
                )

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
