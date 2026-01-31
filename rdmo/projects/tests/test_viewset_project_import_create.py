import json

import pytest

from django.contrib.auth.models import Group, User
from django.urls import reverse

from ..models import Project
from .test_viewset_project import users

urlnames = {
    "import-create-preview": "v1-projects:project-import-create-preview",
    "import-create-confirm": "v1-projects:project-import-create-confirm",
}


@pytest.mark.parametrize('username,password', users)
def test_project_import_create_preview(db, api_client, settings, username, password, xml_path_project):
    if password:
        api_client.login(username=username, password=password)

    url = reverse(urlnames["import-create-preview"])
    projects_count = Project.objects.all().count()

    with open(xml_path_project, 'rb') as xml_file:
        response = api_client.post(url, {'file': xml_file, 'format': 'xml'}, format="multipart")

    if password:
        if response.status_code != 200:
            print(response.json())
        assert response.status_code == 200
        data = json.loads(response.content.decode())
        # Preview response should include at least one value and one snapshot
        assert 'values' in data
        assert len(data['values']) > 0
        assert 'snapshots' in data
        assert len(data['snapshots']) > 0
        assert projects_count == Project.objects.all().count()
    else:
        # Anonymous user -> 401 Unauthorized
        assert response.status_code == 401


@pytest.mark.parametrize('action', ['preview','confirm'])
def test_import_create_preview_and_confirm_get_not_allowed(db, client, action):
    username = password = 'admin'
    client.login(username=username, password=password)
    url = reverse(urlnames[f"import-create-{action}"])
    response = client.get(url)
    assert response.status_code == 405


def test_import_create_preview_missing_file(db, client):
    username = password = 'user'
    client.login(username=username, password=password)

    url = reverse(urlnames["import-create-preview"])
    resp = client.post(url, {'format': 'xml'})  # no 'file' key
    assert resp.status_code == 400


def test_import_create_preview_invalid_xml(db, client, settings, xml_path_error):
    username = password = 'user'
    client.login(username=username, password=password)

    url = reverse(urlnames["import-create-preview"])

    with open(xml_path_error, "rb") as f:
        resp = client.post(url, {"file": f, "format": "xml"})
    assert resp.status_code == 400
    print(resp.json())
    assert 'Parsing error' in ' '.join(resp.json()['file'])


@pytest.mark.parametrize('username,password', users)
def test_project_import_create_confirm(db, client, settings, username, password, xml_path_project):
    if password:
        client.login(username=username, password=password)
    preview_url = reverse(urlnames["import-create-preview"])
    confirm_url = reverse(urlnames["import-create-confirm"])
    projects_count = Project.objects.all().count()
    if password:
        with open(xml_path_project, 'rb') as xml_file:
            preview_response = client.post(preview_url, {'file': xml_file, 'format': 'xml'})
        assert preview_response.status_code == 200
        preview_data = json.loads(preview_response.content.decode())
        # Prepare payload with all values and snapshots checked (selected)
        # Include the file again for the confirm step
        with open(xml_path_project, 'rb') as xml_file:
            confirm_payload = {
                "file": xml_file,
                "format": "xml",
                "checked_values": [v["key"] for v in preview_data.get("values", [])],
                "checked_snapshots": [s["index"] for s in preview_data.get("snapshots", [])],
            }
            confirm_response = client.post(confirm_url, confirm_payload)

        assert confirm_response.status_code == 201
        result = json.loads(confirm_response.content.decode())
        assert 'id' in result
        assert projects_count + 1  == Project.objects.all().count()
    else:
        with open(xml_path_project, 'rb') as xml_file:
            confirm_response = client.post(confirm_url, {'file': xml_file})
        assert confirm_response.status_code == 401


def test_import_create_confirm_restricted(db, client, settings, xml_path_project):
    settings.PROJECT_CREATE_RESTRICTED = True
    settings.PROJECT_CREATE_GROUPS = ['projects']

    username = password = 'user'
    grp = Group.objects.create(name='projects')
    user = User.objects.get(username=username)
    user.groups.add(grp)
    client.login(username=username, password=password)

    preview_url = reverse(urlnames["import-create-preview"])
    confirm_url = reverse(urlnames["import-create-confirm"])
    projects_count = Project.objects.all().count()

    with open(xml_path_project, 'rb') as xml:
        preview_resp = client.post(preview_url, {'file': xml, 'format': 'xml'})
    assert preview_resp.status_code == 200
    preview_data = preview_resp.json()

    with open(xml_path_project, 'rb') as xml:
        confirm_resp = client.post(confirm_url, {
            'file': xml,
            'format': 'xml',
            'checked_values': [v["key"] for v in preview_data.get("values", [])],
            'checked_snapshots': [s["index"] for s in preview_data.get("snapshots", [])],
        })
    assert confirm_resp.status_code == 201
    result = confirm_resp.json()
    assert 'id' in result
    assert projects_count + 1 == Project.objects.all().count()


def test_import_create_confirm_forbidden(db, client, settings, xml_path_project):
    settings.PROJECT_CREATE_RESTRICTED = True
    # no PROJECT_CREATE_GROUPS defined → no one is allowed

    client.login(username='user', password='user')
    preview_url = reverse(urlnames["import-create-preview"])
    confirm_url = reverse(urlnames["import-create-confirm"])
    projects_count = Project.objects.all().count()

    with open(xml_path_project, 'rb') as xml:
        preview_resp = client.post(preview_url, {'file': xml, 'format': 'xml'})
    assert preview_resp.status_code == 403

    with open(xml_path_project, 'rb') as xml:
        confirm_resp = client.post(confirm_url, {
            'file': xml,
            'format': 'xml',
            'checked_values': [],
            'checked_snapshots': [],
        })
    assert confirm_resp.status_code == 403
    assert projects_count == Project.objects.all().count()
