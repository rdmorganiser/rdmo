import json
import os

import pytest

from django.urls import reverse

from .test_viewset_project import view_project_permission_map

# Define test users and their passwords (None for anonymous)
users = (
    ('owner', 'owner'),
    ('manager', 'manager'),
    ('author', 'author'),
    ('guest', 'guest'),
    ('user', 'user'),       # logged-in user with no project membership
    ('site', 'site'),       # staff/site manager user
    ('anonymous', None),    # not logged in
)


urlnames = {
    "upload_accept": "v1-projects:project-upload-accept",
    "imports": "v1-projects:project-imports",
    "import-create-preview": "v1-projects:project-import-create-preview",
    "import-create-confirm": "v1-projects:project-import-create-confirm",
}


@pytest.mark.parametrize('username,password', users)
def test_project_import_preview(db, client, settings, username, password):
    """Test the import_preview endpoint with various user roles."""
    # Authenticate as the given user (if password is None, remain anonymous)
    if password:
        client.login(username=username, password=password)
    url = reverse(urlnames["import-create-preview"])
    xml_path = os.path.join(settings.BASE_DIR, 'xml', 'project.xml')
    with open(xml_path, 'rb') as xml_file:
        response = client.post(url, {'file': xml_file, 'format': 'xml'})
    if password:
        if username in set(view_project_permission_map):
            # Authorized roles: expect HTTP 200 with preview data
            assert response.status_code == 200
            data = json.loads(response.content.decode())
            # Preview response should include at least one value and one snapshot
            assert 'values' in data
            assert len(data['values']) > 0
            assert 'snapshots' in data
            assert len(data['snapshots']) > 0
        else:
            # Logged in but not permitted (author/guest/normal user) -> 403 Forbidden
            assert response.status_code == 403
    else:
        # Anonymous user -> 401 Unauthorized
        assert response.status_code == 401

@pytest.mark.parametrize('username,password', users)
def test_project_import_confirm(db, client, settings, username, password):
    """Test the import_confirm endpoint with various user roles."""
    # Authenticate as the given user (if password is None, remain anonymous)
    if password:
        client.login(username=username, password=password)
    preview_url = reverse(urlnames["import-create-preview"])
    confirm_url = reverse(urlnames["import-create-confirm"])
    xml_path = os.path.join(settings.BASE_DIR, 'xml', 'project.xml')
    if password and username in view_project_permission_map:
        # Perform preview step to get values/snapshots for authorized users
        with open(xml_path, 'rb') as xml_file:
            preview_response = client.post(preview_url, {'file': xml_file, 'format': 'xml'})
        assert preview_response.status_code == 200
        preview_data = json.loads(preview_response.content.decode())
        # Prepare payload with all values and snapshots checked (selected)
        # Include the file again for the confirm step
        with open(xml_path, 'rb') as xml_file:
            confirm_response = client.post(confirm_url, {**preview_data, 'file': xml_file})
        # Confirm should succeed with HTTP 201 and return new project details
        assert confirm_response.status_code == 201
        result = json.loads(confirm_response.content.decode())
        assert 'id' in result
        assert 'title' in result
    else:
        # Unauthorized roles or anonymous: attempt confirm (should be rejected)
        with open(xml_path, 'rb') as xml_file:
            confirm_response = client.post(confirm_url, {'file': xml_file})
        if password:
            # Logged in but not allowed -> 403 Forbidden
            assert confirm_response.status_code == 403
        else:
            # Not authenticated -> 401 Unauthorized
            assert confirm_response.status_code == 401
