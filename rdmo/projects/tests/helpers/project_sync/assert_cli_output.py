from rdmo.projects.models import Project

PROJECT_SHOW_TEMPLATE = 'Project "{}" [id={}]:'

def assert_sync_projects_show_has_output(out_lines: list[str]):
    """
    Assert that all expected project show headers and required '- Tasks:' and '- Views:' markers
    are present in the CLI output lines.
    """
    out_lines_projects = {i for i in out_lines if i.startswith('Project')}

    expected_project_headers = [
        PROJECT_SHOW_TEMPLATE.format(project.title, project.id)
        for project in Project.objects.all()
    ]

    assert all(header in out_lines_projects for header in expected_project_headers)

    assert any(line == '- Tasks:' for line in out_lines)
    assert any(line == '- Views:' for line in out_lines)
