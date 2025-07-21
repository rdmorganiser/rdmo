import pytest

from django.urls import reverse

from ..models import Project

users = (
    ('owner', 'owner'),
    ('manager', 'manager'),
    ('author', 'author'),
    ('guest', 'guest'),
    ('api', 'api'),
    ('user', 'user'),
    ('site', 'site'),
    ('anonymous', None),
)

view_progress_permission_map = {
    'owner': [1, 2, 3, 4, 5, 10],
    'manager': [1, 3, 5, 7],
    'author': [1, 3, 5, 8],
    'guest': [1, 3, 5, 9],
    'api': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    'site': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
}

change_progress_permission_map = {
    'owner': [1, 2, 3, 4, 5, 10],
    'manager': [1, 3, 5, 7],
    'author': [1, 3, 5, 8],
    'api': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    'site': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
}

urlnames = {
    'navigation': 'v1-projects:project-navigation'
}

projects = [1, 2, 3, 4, 5]
sections = [1]


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_navigation_get(db, client, username, password, project_id):
    client.login(username=username, password=password)

    project = Project.objects.get(id=project_id)
    sections = project.catalog.sections.order_by("section_catalogs").all()

    if project_id in view_progress_permission_map.get(username, []):
        catalog_elements = project.catalog.elements
        for section in sections:
            url = reverse(urlnames['navigation'], args=[project_id]) + f'{section.id}/'
            response = client.get(url)
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            assert len(catalog_elements) == len(data)

    else:
        if sections:
            section_id = sections[0].id
            url = reverse(urlnames['navigation'], args=[project_id]) + f'{section_id}/'
            response = client.get(url)
            if password:
                assert response.status_code == 404
            else:
                assert response.status_code == 401
