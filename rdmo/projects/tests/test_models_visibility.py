import pytest

from django.contrib.sites.models import Site

from ..models import Project, Visibility

project_id = 12


def test_visibility_remove_model(db):
    project = Project.objects.get(id=12)
    project.visibility.sites.set([1, 2, 3])

    project.visibility.remove_site(Site.objects.get(id=1))

    project.refresh_from_db()

    assert {site.id for site in project.visibility.sites.all()} == {2, 3}


def test_visibility_remove_model_empty(db):
    project = Project.objects.get(id=12)
    project.visibility.sites.clear()

    project.visibility.remove_site(Site.objects.get(id=1))

    project.refresh_from_db()

    assert {site.id for site in project.visibility.sites.all()} == {2, 3}


def test_visibility_remove_model_last(db):
    project = Project.objects.get(id=12)
    project.visibility.sites.set([1])

    project.visibility.remove_site(Site.objects.get(id=1))

    project.refresh_from_db()

    with pytest.raises(Visibility.DoesNotExist):
        assert project.visibility
