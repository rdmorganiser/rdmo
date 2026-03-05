from django.db.models import OuterRef, Subquery
from django.db.models.functions import Coalesce, Greatest

from rdmo.projects.models import Project, Value


def get_projects_ordered_by_last_changed():
    return Project.objects.annotate(
        last_changed=Coalesce(Greatest(Subquery(
            Value.objects.filter(project=OuterRef('pk')).order_by('-updated').values('updated')[:1]
        ), 'updated'), 'updated')
    ).order_by('last_changed')
