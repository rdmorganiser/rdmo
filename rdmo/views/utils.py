def build_project_tree(projects):
    return [{
        'id': project.id,
        'children': build_project_tree(project.get_children())
    } for project in projects]
