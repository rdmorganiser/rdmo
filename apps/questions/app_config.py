from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class QuestionsConfig(AppConfig):
    name = 'apps.questions'
    verbose_name = _('Questions')
