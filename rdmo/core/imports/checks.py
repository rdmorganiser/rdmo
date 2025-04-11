import logging
from typing import Optional

from django.db import models
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)

def check_permissions(instance: models.Model, element_uri: str, user: models.Model) -> Optional[str]:
    if user is None:
        return

    app_label = instance._meta.app_label
    model_name = instance._meta.model_name

    if instance.id:
        perms = [f'{app_label}.change_{model_name}_object']
    else:
        perms = [f'{app_label}.add_{model_name}_object']

    if not user.has_perms(perms, instance):
        message = _('You have no permissions to import') + f' {instance._meta.object_name} {element_uri}.'
        logger.info(message)
        return message
