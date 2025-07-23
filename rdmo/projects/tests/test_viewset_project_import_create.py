import json
import os

import pytest

from django.contrib.auth.models import Group, User
from django.urls import reverse

from .test_viewset_project import change_project_permission_map, projects, users, view_project_permission_map

urlnames = {
    "upload_accept": "v1-projects:project-upload-accept",
    "imports": "v1-projects:project-imports",
    "import-create-preview": "v1-projects:project-import-create-preview",
    "import-create-confirm": "v1-projects:project-import-create-confirm",
    "import-update-preview": "v1-projects:project-import-update-preview",
    "import-update-confirm": "v1-projects:project-import-update-confirm",
}

def test_import_create_preview_get_not_allowed(db, client):
    username = password = 'user'
    client.login(username=username, password=password)

    url = reverse(urlnames["import-create-preview"])
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.parametrize('username,password', users)
def test_project_import_create_preview(db, client, settings, username, password):
    """Test the import_preview endpoint with various user roles."""
    # Authenticate as the given user (if password is None, remain anonymous)
    if password:
        client.login(username=username, password=password)

    url = reverse(urlnames["import-create-preview"])
    xml_path = os.path.join(settings.BASE_DIR, 'xml', 'project.xml')
    with open(xml_path, 'rb') as xml_file:
        response = client.post(url, {'file': xml_file, 'format': 'xml'})

    if password:
        # Authorized roles: expect HTTP 200 with preview data
        assert response.status_code == 200
        data = json.loads(response.content.decode())
        # Preview response should include at least one value and one snapshot
        assert 'values' in data
        assert len(data['values']) > 0
        assert 'snapshots' in data
        assert len(data['snapshots']) > 0
    else:
        # Anonymous user -> 401 Unauthorized
        assert response.status_code == 401


def test_import_create_preview_missing_file(db, client):
    username = password = 'user'
    client.login(username=username, password=password)

    url = reverse(urlnames["import-create-preview"])
    resp = client.post(url, {'format': 'xml'})  # no 'file' key
    assert resp.status_code == 400


def test_import_create_preview_invalid_xml(db, client, settings):
    username = password = 'user'
    client.login(username=username, password=password)

    url = reverse(urlnames["import-create-preview"])
    bad_xml = os.path.join(settings.BASE_DIR, "xml", "error.xml")
    with open(bad_xml, "rb") as f:
        resp = client.post(url, {"file": f, "format": "xml"})
    assert resp.status_code == 400
    assert 'Parsing error' in ' '.join(resp.json()['file'])


@pytest.mark.parametrize('username,password', users)
def test_project_import_create_confirm(db, client, settings, username, password):
    """Test the import_confirm endpoint with various user roles."""
    # Authenticate as the given user (if password is None, remain anonymous)
    if password:
        client.login(username=username, password=password)
    preview_url = reverse(urlnames["import-create-preview"])
    confirm_url = reverse(urlnames["import-create-confirm"])
    xml_path = os.path.join(settings.BASE_DIR, 'xml', 'project.xml')
    if password:
        # Perform preview step to get values/snapshots for authorized users
        with open(xml_path, 'rb') as xml_file:
            preview_response = client.post(preview_url, {'file': xml_file, 'format': 'xml'})
        assert preview_response.status_code == 200
        preview_data = json.loads(preview_response.content.decode())
        # Prepare pacyload with all values and snapshots checked (selected)
        # Include the file again for the confirm step
        with open(xml_path, 'rb') as xml_file:
            confirm_payload = {
                "file": xml_file,
                "format": "xml",
                "checked_values": [v["key"] for v in preview_data.get("values", [])],
                "checked_snapshots": [s["index"] for s in preview_data.get("snapshots", [])],
            }
            confirm_response = client.post(confirm_url, confirm_payload)
        # Confirm should succeed with HTTP 201 and return new project details
        assert confirm_response.status_code == 201
        result = json.loads(confirm_response.content.decode())
        assert 'id' in result
        assert 'title' in result
    else:
        # Unauthorized roles or anonymous: attempt confirm (should be rejected)
        with open(xml_path, 'rb') as xml_file:
            confirm_response = client.post(confirm_url, {'file': xml_file})
        assert confirm_response.status_code == 401


def test_import_create_confirm_get_not_allowed(db, client):
    username = password = "user"
    client.login(username=username, password=password)

    url = reverse(urlnames["import-create-confirm"])
    response = client.get(url)
    assert response.status_code == 403


def test_import_create_confirm_restricted(db, client, settings):
    """
    When PROJECT_CREATE_RESTRICTED=True, only users in PROJECT_CREATE_GROUPS
    may hit import-create-preview (200) and then import-create-confirm (201).
    Others (including anon) get 403 or 401.
    """
    settings.PROJECT_CREATE_RESTRICTED = True
    settings.PROJECT_CREATE_GROUPS = ['projects']

    # ensure 'projects' group exists and assign to logged-in user
    username = password = 'user'
    grp = Group.objects.create(name='projects')
    user = User.objects.get(username=username)
    user.groups.add(grp)
    client.login(username=username, password=password)

    preview_url = reverse(urlnames["import-create-preview"])
    confirm_url = reverse(urlnames["import-create-confirm"])
    xml_path = os.path.join(settings.BASE_DIR, 'xml', 'project.xml')

    # Preview step
    with open(xml_path, 'rb') as xml:
        preview_resp = client.post(preview_url, {'file': xml, 'format': 'xml'})
    assert preview_resp.status_code == 200
    preview_data = preview_resp.json()

    with open(xml_path, 'rb') as xml:
        confirm_resp = client.post(confirm_url, {
            'file': xml,
            'format': 'xml',
            'checked_values': [v["key"] for v in preview_data.get("values", [])],
            'checked_snapshots': [s["index"] for s in preview_data.get("snapshots", [])],
        })
    assert confirm_resp.status_code == 201
    result = confirm_resp.json()
    assert 'id' in result
    assert 'title' in result


def test_import_create_confirm_forbidden(db, client, settings):
    """
    If PROJECT_CREATE_RESTRICTED=True and the user is NOT in PROJECT_CREATE_GROUPS,
    import-create-preview and import-create-confirm must both 403.
    """
    settings.PROJECT_CREATE_RESTRICTED = True
    # no PROJECT_CREATE_GROUPS defined → no one is allowed

    client.login(username='user', password='user')
    preview_url = reverse(urlnames["import-create-preview"])
    confirm_url = reverse(urlnames["import-create-confirm"])
    xml_path = os.path.join(settings.BASE_DIR, 'xml', 'project.xml')

    with open(xml_path, 'rb') as xml:
        preview_resp = client.post(preview_url, {'file': xml, 'format': 'xml'})
    assert preview_resp.status_code == 403

    with open(xml_path, 'rb') as xml:
        confirm_resp = client.post(confirm_url, {
            'file': xml,
            'format': 'xml',
            'checked_values': [],
            'checked_snapshots': [],
        })
    assert confirm_resp.status_code == 403


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_import_update_preview(db, client, settings, username, password, project_id):
    """Test the import-update-preview endpoint with various user roles."""
    if password:
        client.login(username=username, password=password)

    url = reverse('v1-projects:project-import-update-preview', args=[project_id])
    xml_path = os.path.join(settings.BASE_DIR, 'xml', 'project.xml')

    with open(xml_path, 'rb') as xml_file:
        response = client.post(url, {'file': xml_file, 'format': 'xml'})

    if project_id in view_project_permission_map.get(username, []):
        assert response.status_code == 200
        data = json.loads(response.content.decode())
        assert 'values' in data
        assert 'snapshots' in data
        assert isinstance(data['values'], list)
        assert isinstance(data['snapshots'], list)
    elif password:
        assert response.status_code == 404
    else:
        assert response.status_code == 401


def test_import_update_preview_invalid_xml(db, client, settings):
    username = password = 'owner'
    client.login(username=username, password=password)

    url = reverse(urlnames["import-update-preview"], args=[1])
    bad_xml = os.path.join(settings.BASE_DIR, "xml", "error.xml")
    with open(bad_xml, "rb") as f:
        resp = client.post(url, {"file": f, "format": "xml"})
    assert resp.status_code == 400
    assert 'Parsing error' in ' '.join(resp.json()['file'])



@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_import_update_confirm(db, client, settings, username, password, project_id):
    """Test the import-update-confirm endpoint with various user roles."""
    if password:
        client.login(username=username, password=password)

    preview_url = reverse('v1-projects:project-import-update-preview', args=[project_id])
    confirm_url = reverse('v1-projects:project-import-update-confirm', args=[project_id])
    xml_path = os.path.join(settings.BASE_DIR, 'xml', 'project.xml')

    if project_id in change_project_permission_map.get(username, []):
        with open(xml_path, 'rb') as xml_file:
            preview_response = client.post(preview_url, {'file': xml_file, 'format': 'xml'})
        assert preview_response.status_code == 200
        preview_data = json.loads(preview_response.content.decode())

        with open(xml_path, 'rb') as xml_file:
            confirm_payload = {
                'file': xml_file,
                'format': 'xml',
                'checked_values': [v["key"] for v in preview_data.get("values", [])],
                'checked_snapshots': [s["index"] for s in preview_data.get("snapshots", [])],
            }
            confirm_response = client.post(confirm_url, confirm_payload)

        assert confirm_response.status_code == 201
        result = json.loads(confirm_response.content.decode())
        assert 'id' in result
        assert 'title' in result
    elif password:
        with open(xml_path, 'rb') as xml_file:
            confirm_response = client.post(
                confirm_url,
                {'file': xml_file,'checked_values': [], 'checked_snapshots': []}
            )

        if project_id in view_project_permission_map.get(username, []):
            assert confirm_response.status_code == 400
        else:
            assert confirm_response.status_code == 404
    else:
        with open(xml_path, 'rb') as xml_file:
            confirm_response = client.post(
                confirm_url,
                {'file': xml_file,'checked_values': [], 'checked_snapshots': []}
            )
        assert confirm_response.status_code == 401
