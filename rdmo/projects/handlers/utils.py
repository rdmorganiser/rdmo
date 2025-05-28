from django.db.models.fields.related import ManyToManyField

from rdmo.tasks.models import Task
from rdmo.views.models import View


def get_related_field_name_for_instance(model, instance):
    if isinstance(instance, View):
        return 'views'
    elif isinstance(instance, Task):
        return 'tasks'


    instance_model = instance.__class__

    # 1. Check reverse relations (from View, Task, etc.)
    for rel in model._meta.related_objects:
        if rel.related_model == instance_model:
            return rel.get_accessor_name()

    # 2. Check direct M2M fields on model
    for field in model._meta.local_many_to_many:
        if isinstance(field, ManyToManyField) and field.related_model == instance_model:
            return field.name

    raise ValueError(f"No related field found on {model} for instance of type {instance_model.__name__}")
