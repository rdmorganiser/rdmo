from django.db import models
from django.utils.translation import gettext_lazy as _


class TaskTypes(models.TextChoices):
    TASK = 'task', _('Task')
    RECOMMENDATION = 'recommendation', _('Recommendation')
    STEP = 'step', _('Step')
    GUIDANCE = 'guidance', _('Guidance')


class TaskAreas(models.TextChoices):
    INTERVIEW = 'interview', _('Interview')
    DOCUMENTS = 'documents', _('Documents')
    SNAPSHOTS = 'snapshots', _('Snapshots')
    INFORMATION = 'information', _('Information')
    MEMBERSHIPS = 'memberships', _('Memberships')
