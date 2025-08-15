import shutil

import pytest

from django.core.management import call_command

from rdmo.projects.models import Membership, Project
from rdmo.projects.tests.helpers.xml import add_memberships_to_xml


@pytest.mark.django_db
@pytest.mark.parametrize("include_memberships", [True, False])
@pytest.mark.parametrize("xml_has_memberships", [True, False])
def test_import_projects_memberships_toggle(tmp_path, project_xml, capsys, include_memberships, xml_has_memberships):

    xml_path = tmp_path / "project_with_members.xml"
    shutil.copyfile(project_xml, xml_path)

    if xml_has_memberships:
        add_memberships_to_xml(
            str(xml_path),
            members=[
                {"role": "owner",  "user": {"username": "owner"}},
                {"role": "author", "user": {"username": "author"}},
                {"role": "guest",  "user": {"username": "guest"}},
            ],
        )

    before = Project.objects.count()

    args = ["import_projects", "--files", str(xml_path)]
    if include_memberships:
        args.append("--include-memberships")

    call_command(*args)
    out = capsys.readouterr().out
    assert "→ Importing" in out
    assert "imported successfully" in out

    assert Project.objects.count() == before + 1
    new_project = Project.objects.order_by("-pk").first()

    expected = {("owner", "owner"), ("author", "author"), ("guest", "guest")}
    if include_memberships and xml_has_memberships:
        actual = {
            (m.user.username, m.role)
            for m in Membership.objects.filter(project=new_project).select_related("user")
        }
        assert actual == expected
    else:
        assert not Membership.objects.filter(project=new_project).exists()


@pytest.mark.django_db
def test_import_projects_from_files_explicit(tmp_path, project_xml, capsys):
    """Import a project via explicit --files path (no memberships)."""
    xml_path = tmp_path / "project.xml"
    shutil.copyfile(project_xml, xml_path)

    before = Project.objects.count()
    call_command("import_projects", "--files", str(xml_path))

    out = capsys.readouterr().out
    assert "→ Importing" in out
    assert "imported successfully" in out
    assert Project.objects.count() == before + 1


@pytest.mark.django_db
def test_import_projects_dir_scan_with_filter_and_missing(tmp_path, project_xml, capsys):
    """
    Import via --dir with one valid numeric folder and one missing.
    Expect a warning and a successful import of the existing one.
    """
    good_id = 42
    (tmp_path / str(good_id)).mkdir(parents=True)
    shutil.copyfile(project_xml, tmp_path / str(good_id) / "project.xml")
    (tmp_path / "999999").mkdir()  # empty folder

    before = Project.objects.count()
    call_command("import_projects", "--dir", str(tmp_path), "--projects", str(good_id), "999999")

    out = capsys.readouterr().out
    assert ("Some projects could not be found" in out) or ('No XML file found' in out)
    assert "imported successfully" in out
    assert Project.objects.count() == before + 1


@pytest.mark.django_db
def test_import_projects_files_skips_non_xml(tmp_path, project_xml, capsys):
    """Passing a non-XML alongside a valid XML: skip with warning, still import XML."""
    good_xml = tmp_path / "project.xml"
    shutil.copyfile(project_xml, good_xml)

    junk = tmp_path / "notes.txt"
    junk.write_text("hello")

    before = Project.objects.count()
    call_command("import_projects", "--files", str(junk), str(good_xml))

    out = capsys.readouterr().out
    assert "Skipping non-XML file" in out
    assert "imported successfully" in out
    assert Project.objects.count() == before + 1


@pytest.mark.django_db
@pytest.mark.parametrize("export_include_memberships", [True, False])
@pytest.mark.parametrize("import_include_memberships", [True, False])
def test_roundtrip_export_then_import_memberships_toggle(
    tmp_path, capsys, export_include_memberships, import_include_memberships
):
    """
    Round-trip: export project id=1 to XML, then import it back.
    Memberships in the imported project should exist iff BOTH:
      - export included memberships, and
      - import requested memberships.
    """
    project = Project.objects.get(id=1)
    src_members = set(
        Membership.objects.filter(project=project)
        .values_list("user_id", "role")
    )
    # --- export ---
    export_args = [
        "export_projects",
        "--projects", str(project.id),
        "--export-mode", "project",
        "--format", "xml",
        "--path", str(tmp_path),
    ]
    if export_include_memberships:
        assert src_members, "should not be empty here"
        export_args.append("--include-memberships")

    call_command(*export_args)

    out = capsys.readouterr().out
    assert "Exported 1 project(s) to" in out

    # --- import ---
    import_args = ["import_projects", "--dir", str(tmp_path)]
    if import_include_memberships:
        import_args.append("--include-memberships")

    before_count = Project.objects.count()
    call_command(*import_args)

    out = capsys.readouterr().out
    assert "→ Importing" in out
    assert "imported successfully" in out

    # a new project must have been created
    assert Project.objects.count() == before_count + 1
    imported = Project.objects.exclude(pk=project.pk).order_by("-pk").first()

    imported_members = set(
        Membership.objects.filter(project=imported)
        .values_list("user_id", "role")
    )

    expect_members = export_include_memberships and import_include_memberships

    if expect_members:
        # imported memberships should match the source memberships (set compare)
        assert imported_members, "should not be empty here"
        assert imported_members == src_members
    else:
        # no memberships should have been imported
        assert imported_members == set()
