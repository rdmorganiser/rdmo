import logging
from pathlib import Path

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.urls import reverse

from rdmo.core.mail import send_mail
from rdmo.core.plugins import get_plugins
from rdmo.core.utils import remove_double_newlines

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


def get_contact_message(request, project):
    project_url = project.get_absolute_url()
    project_interview_url = reverse('project_interview', args=[project.id])

    context = {
        'user': request.user,
        'site': Site.objects.get_current(),
        'project': project,
        'project_url': request.build_absolute_uri(project_url)
    }

    page_id = request.GET.get('page')
    if page_id:
        page = project.catalog.get_page(page_id)
        if page:
            context.update({
                'page': page,
                'page_url': request.build_absolute_uri(f'{project_interview_url}{page_id}/')
            })

    questionset_id = request.GET.get('questionset')
    if questionset_id:
        context['questionset'] = project.catalog.get_questionset(questionset_id)

    question_id = request.GET.get('question')
    if question_id:
        context['question'] = project.catalog.get_question(question_id)

    value_ids = request.GET.getlist('values')
    if value_ids:
        values = project.values.filter(snapshot=None).filter(id__in=value_ids)
        context['values'] = values

        if page_id and page and page.is_collection and page.attribute is not None:
            value = values.filter(set_prefix='').first()
            if value:
                try:
                    context['set_value'] = project.values.filter(snapshot=None).get(
                        attribute=page.attribute,
                        set_prefix='',
                        set_index=value.set_index,
                        collection_index=0
                    )
                except ObjectDoesNotExist:
                    pass

    subject = render_to_string('projects/email/project_contact_subject.txt', context)
    message = render_to_string('projects/email/project_contact_message.txt', context)

    return {
        'subject': subject,
        'message': remove_double_newlines(message)
    }


def send_contact_message(request, subject, message):
    send_mail(subject, message,
              to=settings.PROJECT_CONTACT_RECIPIENTS,
              cc=[request.user.email], reply_to=[request.user.email])
