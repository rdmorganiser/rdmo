from django.contrib.auth.models import Group
from django.db.models import ForeignKey, ManyToManyField, Model

from rdmo.projects.models import Project
from rdmo.tasks.models import Task
from rdmo.views.models import View


def get_related_field_name_for_instance(model, instance_or_model) -> str:

    # Normalize to model class if an instance is passed
    instance_model = instance_or_model.__class__ if isinstance(instance_or_model, Model) else instance_or_model

    # Special case checks
    if model is Project and instance_model is View:
        return 'views'
    elif model is Project and instance_model is Task:
        return 'tasks'
    elif model is Project and instance_model is Group:
        return 'groups'

    # 1. Check reverse relations (related objects from other models pointing to `model`)
    for rel in model._meta.related_objects:
        if rel.related_model == instance_model:
            return rel.get_accessor_name()

    # 2. Check direct ForeignKey fields
    for field in model._meta.fields:
        if isinstance(field, ForeignKey) and field.related_model == instance_model:
            return field.name

    # 3. Check direct ManyToMany fields
    for field in model._meta.local_many_to_many:
        if isinstance(field, ManyToManyField) and field.related_model == instance_model:
            return field.name

    raise ValueError(f"No related field found on {model} for {instance_model}")
