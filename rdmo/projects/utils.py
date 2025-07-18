import logging
import mimetypes
from collections import defaultdict
from collections.abc import Iterable
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.timezone import now

from rdmo.accounts.utils import make_unique_username
from rdmo.core.mail import send_mail
from rdmo.core.plugins import get_plugins
from rdmo.core.utils import remove_double_newlines
from rdmo.projects.models import Membership, Project

logger = logging.getLogger(__name__)
User = get_user_model()

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


def check_options(project, value):
    # loop over all values of a question and check if value.option matches the optionsets of the question
    for question in filter(lambda q: q.attribute == value.attribute, project.catalog.questions):
        question_options = [
            option.id
            for optionset in question.optionsets.all()
            for option in optionset.options.all()
        ]

        # fail if question requires an option but value has none
        if question_options and value.option is None:
            return False

        # fail if the value's option is not allowed for this question
        if value.option is not None and value.option.id not in question_options:
            return False

    return True


def copy_project(instance, site, owners):
    from .models import Membership, Project, Value  # to prevent circular inclusion

    timestamp = now()

    tasks = instance.tasks.all()
    views = instance.views.all()

    values = instance.values.filter(snapshot=None)
    snapshots = {
        snapshot: instance.values.filter(snapshot=snapshot)
        for snapshot in instance.snapshots.all()
    }

    # a completely new project instance needs to be created in order for mptt to work
    project = Project.objects.create(
        parent=instance.parent,
        site=site,
        title=instance.title,
        description=instance.description,
        catalog=instance.catalog,
        created=timestamp
    )

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
            # file values cannot be bulk created since we need their id and only postgres provides that (reliably)
            # https://docs.djangoproject.com/en/4.2/ref/models/querysets/#bulk-create
            value.save()
            value.copy_file(value.file_name, value.file)
        else:
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
                value.save()
                value.copy_file(value.file_name, value.file)
            else:
                project_snapshot_values.append(value)

        # insert the new snapshot values using bulk_create
        Value.objects.bulk_create(project_snapshot_values)

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
    accept = defaultdict(set)
    for import_plugin in get_plugins('PROJECT_IMPORTS').values():
        if isinstance(import_plugin.accept, dict):
            for mime_type, suffixes in import_plugin.accept.items():
                accept[mime_type].update(suffixes)

        elif isinstance(import_plugin.accept, str):
            # legacy fallback for pre 2.3.0 RDMO, e.g. `accept = '.xml'`
            suffix = import_plugin.accept
            mime_type, encoding = mimetypes.guess_type(f'example{suffix}')
            if mime_type:
                accept[mime_type].update([suffix])

        elif import_plugin.upload is True:
            # if one of the plugins does not have the accept field, but is marked as upload plugin
            # all file types are allowed
            return {}

    return accept


def compute_set_prefix_from_set_value(set_value, value):
    set_prefix_length = len(set_value.set_prefix.split('|')) if set_value.set_prefix else 0
    return '|'.join([
        str(set_value.set_index) if (index == set_prefix_length) else value
        for index, value in enumerate(value.set_prefix.split('|'))
    ])


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


def import_memberships(project: Project, records: Iterable[dict], create_users: bool = True) -> tuple[int, int]:
    """
    Assigns Memberships on `project` based on `records`.

    Each record may include 'user_id', 'email', 'username',
    'first_name', 'last_name', 'role', etc.

    If create_users=False, any record for which no existing User
    can be found will raise ValidationError.  Otherwise, missing
    users will be auto-created (with unusable password).

    Returns: (created_count, skipped_count)
    """
    created = skipped = 0

    for rec in records:
        # 1) find or (optionally) create user
        user = None

        # a) by PK
        user_id = rec.get("user_id")
        if user_id is not None:
            user = User.objects.filter(pk=user_id).first()

        # b) by email
        email = (rec.get("email") or "").lower()
        if not user and email:
            user = User.objects.filter(email__iexact=email).first()

        # c) by username
        username = rec.get("username")
        if not user and username:
            user = User.objects.filter(username=username).first()

        if not user:
            if not create_users:
                raise ValidationError(f"No existing user for record {rec!r}")
            # auto-create
            desired = username or (email.split("@")[0] if email else "")
            username = make_unique_username(desired)
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=rec.get("first_name", ""),
                last_name=rec.get("last_name", ""),
                is_active=True,
            )
            user.set_unusable_password()
            user.save(update_fields=["password"])
            if username != desired:
                logger.info("Username '%s' taken, created unique name '%s'.", desired, username)

        # 2) assign Membership
        role = rec.get("role") or "guest"
        try:
            Membership.objects.update_or_create(project=project, user=user, defaults={"role": role})
        except IntegrityError as exc:
            logger.warning("Duplicate membership %s / %s: %s", project.pk, user.pk, exc)
            skipped += 1
        else:
            created += 1

    return created, skipped
