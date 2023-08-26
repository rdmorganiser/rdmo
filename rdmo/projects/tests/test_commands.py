import io

import pytest

from django.core.management import call_command
from django.core.management.base import CommandError

from rdmo.projects.models import Project

projects_without_owner = [6, 7, 8, 9, 11]

prune_assignments = [
    ('guest', "['owner', 'guest', 'author', 'manager']", [6, 11]),
    ('author', "['owner', 'author', 'manager']", [6, 9, 11]),
    ('manager', "['owner', 'manager']", [6, 8, 9, 11]),
    ('owner', "['owner']", projects_without_owner)
]

def get_prune_output(projects, remove=False):
    project_output = ""
    for proj in projects:
        project_output += f'{proj.title} (id={proj.id})\n'
        if remove:
            project_output += "...removing...OK\n"
    return project_output


def test_prune_projects_error(db, settings):
    stdout, stderr = io.StringIO(), io.StringIO()

    with pytest.raises(CommandError) as e:
        call_command('prune_projects', '--min_role', 'unknown', stdout=stdout, stderr=stderr)

    assert str(e.value) == 'Role "unknown" does not exist'


@pytest.mark.parametrize('min_role,role_list,projects', prune_assignments)
def test_prune_projects_output(db, settings, min_role, role_list, projects):
    stdout, stderr = io.StringIO(), io.StringIO()

    instances = Project.objects.filter(id__in=projects).all()
    call_command('prune_projects', '--min_role', min_role, stdout=stdout, stderr=stderr)

    assert stdout.getvalue() == \
        f"Found projects without {role_list}:\n{get_prune_output(instances)}"
    assert not stderr.getvalue()


def test_prune_projects_output2(db, settings):
    stdout, stderr = io.StringIO(), io.StringIO()

    instances = Project.objects.filter(id__in=projects_without_owner)
    call_command('prune_projects', stdout=stdout, stderr=stderr)

    assert stdout.getvalue() == \
        "Found projects without ['owner']:\n%s" % (get_prune_output(instances))
    assert not stderr.getvalue()


def test_prune_projects_remove(db, settings):
    stdout, stderr = io.StringIO(), io.StringIO()

    instances = list(Project.objects.filter(id__in=projects_without_owner).all()).copy()

    call_command('prune_projects', '--remove', stdout=stdout, stderr=stderr)

    std_output = stdout.getvalue()
    prune_output = "Found projects without ['owner']:\n%s" % (get_prune_output(instances, True))

    assert std_output == prune_output
    assert not stderr.getvalue()

    stdout, stderr = io.StringIO(), io.StringIO()
    call_command('prune_projects', '--remove', stdout=stdout, stderr=stderr)

    assert stdout.getvalue() == "No projects without ['owner']\n"
    assert not stderr.getvalue()
