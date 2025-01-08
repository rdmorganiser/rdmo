

def remove_instance_from_projects(projects, project_field, instance):
    for project in projects:
        getattr(project, project_field).remove(instance)


def add_instance_to_projects(projects, project_field, instance):
    for project in projects:
        getattr(project, project_field).add(instance)
