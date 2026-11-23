from rdmo.projects.models import Project


def project_relation_ids(field):
    return {
        project.pk: set(getattr(project, field).values_list('id', flat=True))
        for project in Project.objects.all()
    }
