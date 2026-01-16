import json

import pytest

from django.urls import reverse

from ..models import Project
from .test_viewset_project import change_project_permission_map, projects, users, view_project_permission_map

urlnames = {
    "import-update-preview": "v1-projects:project-import-update-preview",
    "import-update-confirm": "v1-projects:project-import-update-confirm",
}


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_import_update_preview(db, api_client, settings, username, password, project_id, xml_path_project):
    if password:
        api_client.login(username=username, password=password)

    url = reverse('v1-projects:project-import-update-preview', args=[project_id])
    projects_count = Project.objects.all().count()

    with open(xml_path_project, 'rb') as xml_file:
        response = api_client.post(url, {'file': xml_file, 'format': 'xml'}, format="multipart")

    if project_id in view_project_permission_map.get(username, []):
        assert response.status_code == 200
        data = json.loads(response.content.decode())
        assert 'values' in data
        assert 'snapshots' in data
        assert isinstance(data['values'], list)
        assert isinstance(data['snapshots'], list)
        assert projects_count == Project.objects.all().count()
    elif password:
        assert response.status_code == 404
    else:
        assert response.status_code == 401


@pytest.mark.parametrize('action', ['preview','confirm'])
def test_import_update_preview_and_confirm_get_not_allowed(db, api_client, action):
    username = password = 'owner'
    api_client.login(username=username, password=password)
    url = reverse(urlnames[f"import-update-{action}"], args=[1])
    response = api_client.get(url)
    assert response.status_code == 405


def test_import_update_preview_invalid_xml(db, client, settings, xml_path_error):
    username = password = 'owner'
    client.login(username=username, password=password)

    url = reverse(urlnames["import-update-preview"], args=[1])
    with open(xml_path_error, "rb") as f:
        resp = client.post(url, {"file": f, "format": "xml"}, format="multipart")
    assert resp.status_code == 400
    assert 'Parsing error' in ' '.join(resp.json()['non_field_errors'])


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_import_update_confirm(db, api_client, settings, username, password, project_id, xml_path_project):
    if password:
        api_client.login(username=username, password=password)

    preview_url = reverse('v1-projects:project-import-update-preview', args=[project_id])
    confirm_url = reverse('v1-projects:project-import-update-confirm', args=[project_id])
    projects_count = Project.objects.all().count()

    if project_id in change_project_permission_map.get(username, []):
        with open(xml_path_project, 'rb') as xml_file:
            preview_response = api_client.post(preview_url, {'file': xml_file, 'format': 'xml'}, format="multipart")
        assert preview_response.status_code == 200
        preview_data = json.loads(preview_response.content.decode())

        with open(xml_path_project, 'rb') as xml_file:
            confirm_payload = {
                'file': xml_file,
                'format': 'xml',
                'checked_values': [v["key"] for v in preview_data.get("values", [])],
                'checked_snapshots': [s["index"] for s in preview_data.get("snapshots", [])],
            }
            confirm_response = api_client.post(confirm_url, confirm_payload)

        assert confirm_response.status_code == 201
        result = json.loads(confirm_response.content.decode())
        assert 'id' in result
        assert 'title' in result
        assert projects_count == Project.objects.all().count()
    elif password:
        with open(xml_path_project, 'rb') as xml_file:
            confirm_response = api_client.post(
                confirm_url,
                {'file': xml_file,'checked_values': [], 'checked_snapshots': []}
            )

        if project_id in view_project_permission_map.get(username, []):
            assert confirm_response.status_code == 400
        else:
            assert confirm_response.status_code == 404
    else:
        with open(xml_path_project, 'rb') as xml_file:
            confirm_response = api_client.post(
                confirm_url,
                {'file': xml_file,'checked_values': [], 'checked_snapshots': []}
            )
        assert confirm_response.status_code == 401
