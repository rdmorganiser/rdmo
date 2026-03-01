from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from rdmo.projects.models import Membership, Project
from rdmo.questions.models import Catalog
from rdmo.tasks.models import Task
from rdmo.views.models import View

project_id = 1
catalog_id = 1
site_id = 1
task_id = 1
view_id = 1


def test_project_membership_change_for_tasks(db, settings):
    settings.PROJECT_TASKS_SYNC = True

    # create a project with tasks
    project = Project.objects.create(
        title='TEST',
        catalog=Catalog.objects.get(id=catalog_id),
        site=Site.objects.get(id=site_id)
    )
    project.tasks.set(Task.objects.filter(sites=site_id))
    project_tasks = {t.id for t in project.tasks.all()}
    assert project_tasks == {t.id for t in Task.objects.filter(sites=site_id)}

    # make one task unavailable
    task = Task.objects.get(id=task_id)
    task.available = False
    task.save()

    # assert that the task was removed
    project.refresh_from_db()
    project_tasks = {t.id for t in project.tasks.all()}
    assert project_tasks == {t.id for t in Task.objects.filter(sites=site_id).exclude(id=task_id)}

    # add an editor
    Membership.objects.create(project=project, user=User.objects.get(username='editor'), role='guest')

    # assert that the task is back
    project.refresh_from_db()
    project_tasks = {t.id for t in project.tasks.all()}
    assert project_tasks == {t.id for t in Task.objects.filter(sites=site_id)}


def test_project_membership_change_for_views(db, settings):
    settings.PROJECT_VIEWS_SYNC = True

    # create a project with views
    project = Project.objects.create(
        title='TEST',
        catalog=Catalog.objects.get(id=catalog_id),
        site=Site.objects.get(id=site_id)
    )
    project.views.set(View.objects.filter(sites=site_id))
    project_views = {t.id for t in project.views.all()}
    assert project_views == {t.id for t in View.objects.filter(sites=site_id)}

    # make one view unavailable
    view = View.objects.get(id=view_id)
    view.available = False
    view.save()

    # assert that the view was removed
    project.refresh_from_db()
    project_views = {t.id for t in project.views.all()}
    assert project_views == {t.id for t in View.objects.filter(sites=site_id).exclude(id=view_id)}

    # add an editor
    Membership.objects.create(project=project, user=User.objects.get(username='editor'), role='guest')

    # assert that the view is back
    project.refresh_from_db()
    project_views = {t.id for t in project.views.all()}
    assert project_views == {t.id for t in View.objects.filter(sites=site_id)}
