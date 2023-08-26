import itertools

import pytest

from django.contrib.auth.models import Group
from django.contrib.sites.models import Site

from rdmo.projects.models import Project
from rdmo.questions.models import Catalog
from rdmo.views.models import View

view_update_tests = [
    # tuples of: view_id, sites, catalogs, groups, project_id, project_exists
    ('3', [],         [],      [], '10', True),
    ('3', [2],        [],      [], '10', False),
    ('3', [1, 2, 3],  [],      [], '10', True),
    ('3', [],         [2],     [], '10', False),
    ('3', [2],        [2],     [], '10', False),
    ('3', [1, 2, 3],  [2],     [], '10', False),
    ('3', [],         [1, 2],  [], '10', True),
    ('3', [2],        [1, 2],  [], '10', False),
    ('3', [1, 2, 3],  [1, 2],  [], '10', True),

    ('3', [],         [],      [1], '10', False),
    ('3', [2],        [],      [1], '10', False),
    ('3', [1, 2, 3],  [],      [1], '10', False),
    ('3', [],         [2],     [1], '10', False),
    ('3', [2],        [2],     [1], '10', False),
    ('3', [1, 2, 3],  [2],     [1], '10', False),
    ('3', [],         [1, 2],  [1], '10', False),
    ('3', [2],        [1, 2],  [1], '10', False),
    ('3', [1, 2, 3],  [1, 2],  [1], '10', False),

    ('3', [],         [],      [1, 2, 3, 4], '10', False),
    ('3', [2],        [],      [1, 2, 3, 4], '10', False),
    ('3', [1, 2, 3],  [],      [1, 2, 3, 4], '10', False),
    ('3', [],         [2],     [1, 2, 3, 4], '10', False),
    ('3', [2],        [2],     [1, 2, 3, 4], '10', False),
    ('3', [1, 2, 3],  [2],     [1, 2, 3, 4], '10', False),
    ('3', [],         [1, 2],  [1, 2, 3, 4], '10', False),
    ('3', [2],        [1, 2],  [1, 2, 3, 4], '10', False),
    ('3', [1, 2, 3],  [1, 2],  [1, 2, 3, 4], '10', False)
]

@pytest.mark.parametrize('view_id,sites,catalogs,groups,project_id,project_exists', view_update_tests)
def test_update_projects(db, view_id, sites, catalogs, groups, project_id, project_exists):
    view = View.objects.get(pk=view_id)

    view.sites.set(Site.objects.filter(pk__in=sites))
    view.catalogs.set(Catalog.objects.filter(pk__in=catalogs))
    view.groups.set(Group.objects.filter(pk__in=groups))

    assert sorted(itertools.chain.from_iterable(view.sites.all().values_list('pk'))) == sites
    assert sorted(itertools.chain.from_iterable(view.catalogs.all().values_list('pk'))) == catalogs
    assert sorted(itertools.chain.from_iterable(view.groups.all().values_list('pk'))) == groups

    if not project_exists:
        with pytest.raises(Project.DoesNotExist):
            Project.objects.filter(views=view).get(pk=project_id)
    else:
        assert Project.objects.filter(views=view).get(pk=project_id)
