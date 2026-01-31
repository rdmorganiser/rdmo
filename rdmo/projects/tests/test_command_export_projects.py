import json
import xml.etree.ElementTree as ET

import pytest

from django.core.management import call_command

from rdmo.projects.models import Project


@pytest.mark.django_db
@pytest.mark.parametrize("export_format", ["xml", "json"])
@pytest.mark.parametrize("include_memberships", [True, False])
def test_export_projects_full_project_xml_and_json(tmp_path, capsys, export_format, include_memberships):
    """
    Full-project export (plugin-based) with xml/json, with and without memberships.
    - Always checks the file exists and has sane structure
    - Additionally checks that memberships are present iff --with-members is passed
    """
    project = Project.objects.get(id=1)

    args = [
        "export_projects",
        "--projects", str(project.id),
        "--format", export_format,
        "--path", str(tmp_path),
        "--export-mode", "project"  # is the default
    ]
    if include_memberships:
        args.append("--include-memberships")

    call_command(*args)

    project_dir = tmp_path / str(project.id)
    assert project_dir.exists(), f"Export dir {project_dir} missing"

    exported = (project_dir / project.title).with_suffix(f".{export_format}")
    assert exported.exists(), "Exported file does not exist."

    content_text = exported.read_text("utf-8")

    if export_format == "xml":
        root = ET.fromstring(content_text.encode("utf-8"))
        assert root.tag == "project"
        child_tags = {c.tag for c in root}
        assert  {"title", "description", "catalog", "values"}.issubset(child_tags)
        if include_memberships:
            assert "memberships" in child_tags
        else:
            assert "memberships" not in child_tags

    else:  # json
        # Basic shape check (existing expectation in your suite)
        try:
            data = json.loads(content_text)
        except json.JSONDecodeError as e:
            pytest.fail(f"JSON export not parseable: {e}")

        if isinstance(data, list):
            # Legacy/list-shaped JSON export
            assert len(data) >= 1
            assert all(set(item.keys()) == {"question", "set", "values"} for item in data)
        else:
            pytest.fail(f"Unexpected JSON root type: {type(data)}")

    out = capsys.readouterr().out
    assert f"Exported 1 project(s) to {tmp_path.resolve()}" in out


@pytest.mark.django_db
def test_export_projects_answers_html(tmp_path, capsys):
    """
    Exercise the answers export (template + render_to_format).
    Validate file path layout: <tmp>/<id>/answers/<file>, and sniff-check for HTML + project title.
    """
    project = Project.objects.get(id=1)
    export_format = "html"

    call_command(
        "export_projects",
        "--export-mode", "answers",
        "--format", export_format,
        "--projects", str(project.id),
        "--path", str(tmp_path),
    )

    # answers go into a dedicated subdir determined by mode selection
    answers_dir = tmp_path / str(project.id) / "answers"
    assert answers_dir.exists()

    exported = (answers_dir / project.title).with_suffix(f'.{export_format}')
    assert exported.exists(), "Exported file does not exist."

    text = exported.read_text("utf-8")

    # Lightweight content checks: looks like HTML and mentions the project title.
    assert "<html" in text.lower()
    assert project.title in text

    out = capsys.readouterr().out
    assert f"Exported 1 project(s) to {tmp_path.resolve()}" in out


@pytest.mark.django_db
def test_export_projects_view_html_creates_file(tmp_path, capsys):
    """
    Optional but handy: exercise the 'view' path too.
    Uses any view linked to the project; validates subdir = <view.uri_path>.
    """
    project = Project.objects.get(id=1)
    export_format = 'html'
    # Pick any view attached to the project; if none, skip (fixture variability).
    view = project.views.order_by("id").first()
    if view is None:
        pytest.skip("No project view available in fixtures")

    call_command(
        "export_projects",
        "--export-mode", "view",
        "--view-uri", view.uri,
        "--format", export_format,
        "--projects", str(project.id),
        "--path", str(tmp_path),
    )

    # View exports use subdir of the view's uri_path; files named via Content-Disposition header
    view_dir = tmp_path / str(project.id) / 'views' / view.uri_path
    assert view_dir.exists()

    exported = (view_dir / project.title).with_suffix(f'.{export_format}')
    assert exported.exists(), "Exported file does not exist."

    text = exported.read_text("utf-8")
    assert "<html" in text.lower()

    out = capsys.readouterr().out
    assert f"Exported 1 project(s) to {tmp_path.resolve()}" in out
